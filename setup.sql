-- Create tables
CREATE TABLE IF NOT EXISTS students (
    id      INTEGER PRIMARY KEY,
    name    TEXT NOT NULL,
    age     INTEGER,
    city    TEXT
);

CREATE TABLE IF NOT EXISTS courses (
    id      INTEGER PRIMARY KEY,
    title   TEXT NOT NULL,
    credits INTEGER
);

CREATE TABLE IF NOT EXISTS enrolments (
    id         INTEGER PRIMARY KEY,
    student_id INTEGER,
    course_id  INTEGER,
    grade      INTEGER,   -- grade out of 100
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id)  REFERENCES courses(id)
);

-- Students
INSERT INTO students (name, age, city) VALUES
    ('Alice', 20, 'Amsterdam'), ('Bob', 22, 'Rotterdam'),
    ('Carol', 21, 'Amsterdam'), ('David', 23, 'Utrecht'),
    ('Emma',  20, 'Amsterdam'), ('Frank', 24, 'Rotterdam'),
    ('Grace', 22, 'Utrecht'),   ('Henry', 21, 'Amsterdam');

-- Courses
INSERT INTO courses (title, credits) VALUES
    ('Introduction to Programming', 3),
    ('Database Fundamentals', 4),
    ('Web Development', 3),
    ('Data Science', 5),
    ('Networking Basics', 3);

-- Enrolments (Note: Henry has no enrolments)
INSERT INTO enrolments (student_id, course_id, grade) VALUES
    (1,1,88),(1,2,75),(2,1,60),(2,3,72),(3,2,90),(3,4,85),
    (4,1,55),(4,2,68),(5,3,77),(5,4,92),(6,2,80),(7,5,65),(7,1,70);

    .header on
.mode column

SELECT 
    students.name AS Student, 
    courses.name AS Course
FROM students
JOIN enrolments ON students.id = enrolments.student_id
JOIN courses ON enrolments.course_id = courses.id;