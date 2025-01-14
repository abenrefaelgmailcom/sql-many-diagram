import sqlite3


# יצירת הטבלאות (שאלה 1)
def create_tables(db_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL UNIQUE,
                hours INTEGER NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                student_id INTEGER,
                course_id INTEGER,
                grade INTEGER NOT NULL,
                PRIMARY KEY (student_id, course_id),
                FOREIGN KEY (student_id) REFERENCES students (student_id),
                FOREIGN KEY (course_id) REFERENCES courses (course_id)
            )
        ''')

        conn.commit()
        print("tables created succssesfully.")

    except sqlite3.Error as e:
        print(f"error: {e}")
    finally:
        conn.close()


# הוספת נתונים לטבלאות (שאלה 2)
def insert_data(db_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # הוספת קורסים
        cursor.executemany('''
            INSERT INTO courses (topic, hours) VALUES (?, ?)
        ''', [("Mathematics", 120), ("Physics", 90)])

        # הוספת תלמידים
        cursor.executemany('''
            INSERT INTO students (name, email) VALUES (?, ?)
        ''', [("Alice", "alice@example.com"), ("Bob", "bob@example.com")])

        # הוספת ציונים
        cursor.executemany('''
            INSERT INTO grades (student_id, course_id, grade) VALUES (?, ?, ?)
        ''', [(1, 1, 85), (1, 2, 90), (2, 1, 78), (2, 2, 88)])

        conn.commit()
        print("הנתונים נוספו בהצלחה.")

    except sqlite3.Error as e:
        print(f"error: {e}")
    finally:
        conn.close()


# חישוב ממוצע ציונים לכל קורס (שאלה 3)
def calculate_average_grades(db_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT c.topic, AVG(g.grade) AS average_grade
            FROM grades g
            JOIN courses c ON g.course_id = c.course_id
            GROUP BY c.topic
        ''')

        results = cursor.fetchall()
        print("avg grades to every course:")
        for row in results:
            print(f"subject: {row[0]}, avg course: {row[1]:.2f}")

    except sqlite3.Error as e:
        print(f"error: {e}")
    finally:
        conn.close()


# הצגת כל הקורסים (שאלה 4)
def show_all_courses(db_name):
    try:
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()

        print("list of all courses:")
        for course in courses:
            print(f"ID: {course['course_id']}, subject: {course['topic']}, hours: {course['hours']}")

    except sqlite3.Error as e:
        print(f"error: {e}")
    finally:
        conn.close()


# הוספת קורס חדש עם בדיקה אם כבר קיים (שאלה 5 + אתגר)
def add_course_with_check(db_name, topic, hours):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM courses WHERE topic = ?", (topic,))
        existing_course = cursor.fetchone()

        if existing_course:
            print("error course with the same name already exist!")
        else:
            cursor.execute("INSERT INTO courses (topic, hours) VALUES (?, ?)", (topic, hours))
            conn.commit()
            print("הקורס נוסף בהצלחה.")

    except sqlite3.Error as e:
        print(f"שגיאה: {e}")
    finally:
        conn.close()


# קריאה לפונקציות
if __name__ == "__main__":
    db_name = "hw_solution4.db"

    # יצירת הטבלאות
    create_tables(db_name)

    # הוספת נתונים לטבלאות
    insert_data(db_name)

    # חישוב ממוצע ציונים לכל קורס
    calculate_average_grades(db_name)

    # הצגת כל הקורסים
    show_all_courses(db_name)

    # הוספת קורס חדש עם קלט מהמשתמש
    topic = input("הכנס את נושא הקורס: ").strip()
    hours = int(input("הכנס את מספר השעות: ").strip())
    add_course_with_check(db_name, topic, hours)
