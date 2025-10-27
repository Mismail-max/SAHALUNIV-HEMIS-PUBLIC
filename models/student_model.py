from config.db import get_connection

# Get all students (not recommended for large tables in production)
def get_students_paginated(limit, offset):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students ORDER BY created_at DESC LIMIT %s OFFSET %s", (limit, offset))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_all_students_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

# Search students
def search_students(query):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM students
        WHERE hemis_reg_number LIKE %s OR name LIKE %s OR student_id LIKE %s OR university LIKE %s
    """, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Insert or update a student
def insert_or_update_student(cursor, row, birth_date, enrollment_date):
    cursor.execute("""
        INSERT INTO students (
            hemis_reg_number, student_id, name, mother_name, sex, birth_date, address, phone, email, 
            emergency_contact, emergency_contact_phone, enrollment_date, certificate_type, school_roll_number, 
            foculty, department, program, academic_year, class_year, semester, status, degree, created_by, 
            updated_by, mode_of_study, instruction_medium, university, national_id, nationality, 
            bachelor_degree_graduate_from
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            student_id=VALUES(student_id),
            name=VALUES(name),
            mother_name=VALUES(mother_name),
            sex=VALUES(sex),
            birth_date=VALUES(birth_date),
            address=VALUES(address),
            phone=VALUES(phone),
            email=VALUES(email),
            emergency_contact=VALUES(emergency_contact),
            emergency_contact_phone=VALUES(emergency_contact_phone),
            enrollment_date=VALUES(enrollment_date),
            certificate_type=VALUES(certificate_type),
            school_roll_number=VALUES(school_roll_number),
            foculty=VALUES(foculty),
            department=VALUES(department),
            program=VALUES(program),
            academic_year=VALUES(academic_year),
            class_year=VALUES(class_year),
            semester=VALUES(semester),
            status=VALUES(status),
            degree=VALUES(degree),
            created_by=VALUES(created_by),
            updated_by=VALUES(updated_by),
            mode_of_study=VALUES(mode_of_study),
            instruction_medium=VALUES(instruction_medium),
            university=VALUES(university),
            national_id=VALUES(national_id),
            nationality=VALUES(nationality),
            bachelor_degree_graduate_from=VALUES(bachelor_degree_graduate_from)
    """, (
        row["hemis_reg_number"], row["student_id"], row["name"], row["mother_name"],
        row["sex"], birth_date, row["address"], row["phone"], row["email"],
        row["emergency_contact"], row["emergency_contact_phone"], enrollment_date,
        row["certificate_type"], row["school_roll_number"], row["foculty"], row["department"],
        row["program"], row["academic_year"], row["class_year"], row["semester"], row["status"],
        row["degree"], row["created_by"], row["updated_by"], row["mode_of_study"],
        row["instruction_medium"], row["university"], row["national_id"], row["nationality"],
        row["bachelor_degree_graduate_from"]
    ))

