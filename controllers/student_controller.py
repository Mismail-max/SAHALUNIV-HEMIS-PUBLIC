from flask import Blueprint, render_template, request, redirect, session, flash
from datetime import datetime
import pandas as pd
import os

from config.db import get_connection
from models.student_model import (
    search_students,
    insert_or_update_student,
    get_students_paginated,
    get_all_students_count
)

student_routes = Blueprint("student", __name__)
STUDENTS_PER_PAGE = 20

def parse_us_date(date_str):
    """
    Parses a date string in MM/DD/YYYY format and returns a date object.

    Args:
        date_str (str): The date string to parse.

    Returns:
        date: A date object corresponding to the input string, or None if the input
        is empty, NaN, or not in the expected format.
    """

    if pd.isna(date_str) or date_str.strip() == "":
        return None
    try:
        return datetime.strptime(date_str.strip(), "%m/%d/%Y").date()
    except ValueError:
        return None
    
@student_routes.route("/", methods=["GET", "POST"])
def index():
    """
    The home page, which displays search results when a search query is posted
    and paginated students when a user is logged in.
    """
    search_results = []
    all_students = []
    message = ""
    page = request.args.get("page", default=1, type=int)
    # per_page = 20
    total_pages = 1

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if request.method == "POST":
            student_id = request.form.get("student_id", "").strip()
            # last_name = request.form.get("last_name", "").strip()

            if not student_id :
                flash("Student ID is required.", "danger")
            else:
                cursor.execute("""
                    SELECT * FROM students
                    WHERE BINARY student_id = %s
                """, (student_id,))
                potential_matches = cursor.fetchall()

                if not potential_matches:
                    flash("No student found with this Student ID.", "danger")
                else:
                    search_results = potential_matches

                    if not search_results:
                        flash("Student ID is valid, but the Last Name doesn't match.", "warning")

        # Show paginated students only when logged in
        if session.get("username"):
            cursor.execute("SELECT COUNT(*) as total FROM students")
            total_count = cursor.fetchone()["total"]
            total_pages = (total_count + STUDENTS_PER_PAGE - 1) // STUDENTS_PER_PAGE

            offset = (page - 1) * STUDENTS_PER_PAGE
            cursor.execute("SELECT * FROM students LIMIT %s OFFSET %s", (STUDENTS_PER_PAGE, offset))
            all_students = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    return render_template(
        "index.html",
        search_results=search_results,
        all_students=all_students,
        message=message,
        page=page,
        total_pages=total_pages
    )


@student_routes.route("/delete/<student_id>", methods=["POST"])
def delete_student(student_id):
    """
    Delete a student record given a HEMIS registration number.
    """
    
    if "username" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE hemis_reg_number = %s", (student_id,))
        conn.commit()
        flash(f"Deleted student with HEMIS registration number {student_id}.", "success")
    except Exception as e:
        print("Error deleting student:", e)
        flash("Error deleting student. Please try again.", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect("/students")

@student_routes.route("/upload", methods=["POST"])
def upload():
    """
    Upload a CSV file containing student records. The CSV file should have a header
    with the following columns:

    - hemis_reg_number
    - student_id
    - name
    - mother_name
    - sex
    - birth_date
    - address
    - phone
    - email
    - emergency_contact
    - emergency_contact_phone
    - enrollment_date
    - certificate_type
    - school_roll_number
    - foculty
    - department
    - program
    - academic_year
    - class_year
    - semester
    - status
    - degree
    - created_at
    - created_by
    - updated_at
    - updated_by
    - mode_of_study
    - instruction_medium
    - university
    - national_id
    - nationality
    - bachelor_degree_graduate_from

    The file is expected to be in the format of a US date (mm/dd/yyyy). The file
    will be uploaded to a directory named "uploads" in the root of the project.

    If the student record already exists in the database, it will be skipped. If
    the student record does not exist, it will be inserted into the database.

    After the upload is complete, the user will be redirected to the home page with
    a flash message indicating the number of students uploaded and skipped.

    :return: Redirect to the home page
    """
    if "username" not in session:
        return redirect("/login")

    file = request.files["file"]
    if not file:
        flash("⚠️ No file selected. Please upload a CSV file.", "warning")
        return redirect("/")

    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    df = pd.read_csv(filepath)
    df = df.where(pd.notnull(df), None)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    inserted = 0
    skipped = 0

    for idx, row in df.iterrows():
        try:
            row = row.to_dict()  # Convert Series to dict

            # Clean the row: convert all 'nan', empty string, or missing values to None
            for key in row:
                val = row[key]
                if pd.isna(val) or str(val).strip().lower() == "nan":
                    row[key] = None
                else:
                    row[key] = str(val).strip()

            birth_date = parse_us_date(row.get("birth_date", ""))
            enrollment_date = parse_us_date(row.get("enrollment_date", ""))

            # Check for existing record using BOTH student_id and name
            cursor.execute(
                """
                SELECT COUNT(*) AS count FROM students 
                WHERE student_id = %s AND name = %s
                """,
                (row.get("student_id"), row.get("name"))
            )
            existing = cursor.fetchone()

            if existing and existing["count"] > 0:
                skipped += 1
                continue  # Skip duplicate

            insert_or_update_student(cursor, row, birth_date, enrollment_date)
            inserted += 1

        except Exception as e:
            print(f"❌ Error processing row {idx + 1}: {e}")
            skipped += 1
            continue
    conn.commit()
    cursor.close()
    conn.close()

    if inserted > 0:
        flash(f"✅ {inserted} students uploaded successfully.", "success")
    if skipped > 0:
        flash(f"⚠️ {skipped} duplicates skipped based on student ID and name.", "warning")
    if inserted == 0 and skipped == 0:
        flash("⚠️ No valid records found in the file.", "info")

    return redirect("/")

@student_routes.route("/students", methods=["GET", "POST"])
def student_records():
    page = request.args.get("page", 1, type=int)
    total_pages = 1
    all_students = []
    page_range = []

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if request.method == "POST":
            student_id = request.form.get("student_id", "").strip()
            if student_id:
                cursor.execute("SELECT * FROM students WHERE student_id LIKE %s", (f"%{student_id}%",))
                all_students = cursor.fetchall()
        else:
            cursor.execute("SELECT COUNT(*) as total FROM students")
            total = cursor.fetchone()["total"]
            total_pages = (total + STUDENTS_PER_PAGE - 1) // STUDENTS_PER_PAGE
            offset = (page - 1) * STUDENTS_PER_PAGE
            cursor.execute("SELECT * FROM students LIMIT %s OFFSET %s", (STUDENTS_PER_PAGE, offset))
            all_students = cursor.fetchall()
            # Create a list of page numbers to show in pagination (first 10)
            page_range = list(range(1, min(10, total_pages) + 1))

    finally:
        cursor.close()
        conn.close()

    return render_template(
        "students_table.html",
        all_students=all_students,
        page=page,
        total_pages=total_pages,
        page_range=page_range
    )
