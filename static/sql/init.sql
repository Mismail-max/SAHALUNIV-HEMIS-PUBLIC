USE hemis;

-- Drop table if needed before recreating (optional for development)
-- DROP TABLE IF EXISTS students;

CREATE TABLE IF NOT EXISTS students (
    hemis_reg_number VARCHAR(100) PRIMARY KEY,
    student_id VARCHAR(100),
    name VARCHAR(500),
    mother_name VARCHAR(500),
    sex VARCHAR(20),
    birth_date DATE,
    address VARCHAR(500),
    phone VARCHAR(100),
    email VARCHAR(500),
    emergency_contact VARCHAR(500),
    emergency_contact_phone VARCHAR(100),
    enrollment_date DATE,
    certificate_type VARCHAR(200),
    school_roll_number VARCHAR(100),
    foculty VARCHAR(500),
    department VARCHAR(500),
    program VARCHAR(500),
    academic_year VARCHAR(100),
    class_year VARCHAR(100),
    semester VARCHAR(100),
    status VARCHAR(100),
    degree VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(500),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(500),
    mode_of_study VARCHAR(200),
    instruction_medium VARCHAR(200),
    university VARCHAR(500),
    national_id VARCHAR(100),
    nationality VARCHAR(200),
    bachelor_degree_graduate_from VARCHAR(500)
);

-- Users table with increased lengths for flexibility
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(200) NOT NULL,
    last_name VARCHAR(200) NOT NULL,
    email VARCHAR(500) NOT NULL,
    username VARCHAR(200) NOT NULL UNIQUE,
    password_hash VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
