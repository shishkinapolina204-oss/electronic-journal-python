import sqlite3

class JournalDB:
    def __init__(self, db_name="school_journal.db"):
        self.db_name = db_name
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    class_name TEXT NOT NULL,
                    grades TEXT DEFAULT '',
                    absences INTEGER DEFAULT 0
                )
            """)
            conn.commit()

    def get_classes(self):
        """Возвращает отсортированный список всех классов в базе."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT class_name FROM students ORDER BY class_name ASC")
            return [row[0] for row in cursor.fetchall()]

    def add_student(self, full_name, class_name):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (full_name, class_name) VALUES (?, ?)",
                (full_name, class_name)
            )
            conn.commit()

    def add_students_bulk(self, names_list, class_name):
        """Массовое добавление списка учеников в класс."""
        with self.connect() as conn:
            cursor = conn.cursor()
            data = [(name.strip(), class_name) for name in names_list if name.strip()]
            cursor.executemany(
                "INSERT INTO students (full_name, class_name) VALUES (?, ?)",
                data
            )
            conn.commit()

    def get_students_by_class(self, class_name):
        """Получает учеников выбранного класса, отсортированных по алфавиту."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, full_name, class_name, grades, absences FROM students WHERE class_name = ? ORDER BY full_name ASC",
                (class_name,)
            )
            return cursor.fetchall()

    def update_student_data(self, student_id, grades_str, absences):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE students SET grades = ?, absences = ? WHERE id = ?",
                (grades_str, absences, student_id)
            )
            conn.commit()

    def clear_quarter_for_class(self, class_name):
        """Очищает оценки и пропуски для всего класса (начало новой четверти)."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE students SET grades = '', absences = 0 WHERE class_name = ?",
                (class_name,)
            )
            conn.commit()

    def delete_student(self, student_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            conn.commit()