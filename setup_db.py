import sqlite3
conn = sqlite3.connect('school_database.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS student_attendance (student_id TEXT, name TEXT, attendance_percentage REAL, pin TEXT)')
c.execute("DELETE FROM student_attendance")
c.execute("INSERT INTO student_attendance VALUES ('S101', 'Alice', 92.5, '1234')")
conn.commit()
conn.close()
print('Database Created!')