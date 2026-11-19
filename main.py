import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import JournalDB
from logic import calculate_average, validate_grade, get_status
from json_manager import export_to_json, export_to_excel_csv


class ElectronicJournalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Электронный журнал успеваемости и посещаемости — КГУ «Жамбылская ОСШ»")
        self.root.geometry("980x580")
        self.db = JournalDB()
        self.current_class = None

        self.show_login_screen()

    def show_login_screen(self):
        """1. Экран авторизации учителя."""
        self.login_frame = tk.Frame(self.root, padx=30, pady=30)
        self.login_frame.pack(expand=True)

        tk.Label(self.login_frame, text="Вход в систему «Электронный журнал»", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.login_frame, text="Логин (по умолчанию: teacher):").pack(anchor="w")
        self.login_entry = tk.Entry(self.login_frame, width=30)
        self.login_entry.insert(0, "teacher")
        self.login_entry.pack(pady=5)

        tk.Label(self.login_frame, text="Пароль (по умолчанию: 1234):").pack(anchor="w")
        self.pass_entry = tk.Entry(self.login_frame, width=30, show="*")
        self.pass_entry.insert(0, "1234")
        self.pass_entry.pack(pady=5)

        tk.Button(self.login_frame, text="Войти", width=20, bg="#2e7d32", fg="white", command=self.check_login).pack(pady=15)

    def check_login(self):
        if self.login_entry.get() == "teacher" and self.pass_entry.get() == "1234":
            self.login_frame.destroy()
            self.show_class_selection()
        else:
            messagebox.showerror("Ошибка доступа", "Неверный логин или пароль!")

    def show_class_selection(self):
        """2. Экран выбора или создания класса."""
        self.class_frame = tk.Frame(self.root, padx=30, pady=30)
        self.class_frame.pack(expand=True)

        tk.Label(self.class_frame, text="Выберите класс для работы", font=("Arial", 14, "bold")).pack(pady=10)

        classes = self.db.get_classes()
        if classes:
            tk.Label(self.class_frame, text="Существующие классы:").pack(anchor="w", pady=(5, 2))
            self.class_combo = ttk.Combobox(self.class_frame, values=classes, state="readonly", width=27)
            self.class_combo.current(0)
            self.class_combo.pack(pady=5)
            tk.Button(
                self.class_frame, text="Открыть журнал класса", width=25,
                bg="#1976d2", fg="white", command=self.open_selected_class
            ).pack(pady=8)

        tk.Label(self.class_frame, text="Или введите новый класс (например, 9А):").pack(anchor="w", pady=(15, 2))
        self.new_class_entry = tk.Entry(self.class_frame, width=30)
        self.new_class_entry.pack(pady=5)
        tk.Button(
            self.class_frame, text="Создать и перейти к журналу", width=25,
            bg="#2e7d32", fg="white", command=self.create_new_class
        ).pack(pady=8)

    def open_selected_class(self):
        self.current_class = self.class_combo.get()
        self.class_frame.destroy()
        self.build_main_ui()

    def create_new_class(self):
        cls_name = self.new_class_entry.get().strip()
        if not cls_name:
            messagebox.showwarning("Внимание", "Введите название класса!")
            return
        self.current_class = cls_name
        self.class_frame.destroy()
        self.build_main_ui()

    def switch_class(self):
        """Возврат к выбору другого класса."""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.show_class_selection()

    def build_main_ui(self):
        """3. Основной интерфейс электронного журнала для выбранного класса."""
        header_frame = tk.Frame(self.root, padx=10, pady=8, bg="#e3f2fd")
        header_frame.pack(fill="x")

        tk.Label(
            header_frame, text=f"Журнал класса: {self.current_class}",
            font=("Arial", 12, "bold"), bg="#e3f2fd", fg="#0d47a1"
        ).pack(side="left", padx=5)

        tk.Button(header_frame, text="← Сменить класс", command=self.switch_class).pack(side="left", padx=15)

        tk.Button(
            header_frame, text="Новая четверть (Очистить оценки)",
            bg="#6a1b9a", fg="white", command=self.clear_quarter
        ).pack(side="right", padx=5)

        top_frame = tk.Frame(self.root, padx=10, pady=8)
        top_frame.pack(fill="x")

        tk.Label(top_frame, text="ФИО ученика:").pack(side="left", padx=5)
        self.name_entry = tk.Entry(top_frame, width=25)
        self.name_entry.pack(side="left", padx=5)

        tk.Button(top_frame, text="Добавить одного", bg="#1976d2", fg="white", command=self.add_student).pack(side="left", padx=4)
        tk.Button(top_frame, text="Добавить списком (весь класс)", bg="#0288d1", fg="white", command=self.open_bulk_add_window).pack(side="left", padx=4)

        tk.Label(top_frame, text="Поиск по фамилии:").pack(side="left", padx=(20, 5))
        self.search_entry = tk.Entry(top_frame, width=18)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.load_students())

        columns = ("id", "num", "name", "grades", "avg", "status", "absences")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15, selectmode="extended")
        self.tree.heading("id", text="ID")
        self.tree.heading("num", text="№")
        self.tree.heading("name", text="ФИО ученика (по алфавиту)")
        self.tree.heading("grades", text="Оценки за четверть")
        self.tree.heading("avg", text="Ср. балл")
        self.tree.heading("status", text="Статус")
        self.tree.heading("absences", text="Пропуски (ч.)")

        self.tree.column("id", width=0, stretch=False)
        self.tree.column("num", width=40, anchor="center")
        self.tree.column("name", width=250)
        self.tree.column("grades", width=210)
        self.tree.column("avg", width=80, anchor="center")
        self.tree.column("status", width=140, anchor="center")
        self.tree.column("absences", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        bottom_frame = tk.Frame(self.root, padx=10, pady=10)
        bottom_frame.pack(fill="x")

        tk.Label(bottom_frame, text="Новый балл (1-10):").pack(side="left", padx=5)
        self.grade_entry = tk.Entry(bottom_frame, width=8)
        self.grade_entry.pack(side="left", padx=5)

        tk.Button(bottom_frame, text="Поставить оценку", command=self.add_grade).pack(side="left", padx=5)
        tk.Button(bottom_frame, text="+1 Пропуск", command=self.add_absence).pack(side="left", padx=5)
        tk.Button(bottom_frame, text="Удалить ученика", bg="#c62828", fg="white", command=self.delete_student).pack(side="left", padx=15)

        tk.Button(bottom_frame, text="Экспорт в Excel", bg="#2e7d32", fg="white", command=self.export_excel).pack(side="right", padx=5)
        tk.Button(bottom_frame, text="Экспорт класса в JSON", bg="#ef6c00", fg="white", command=self.export_json).pack(side="right", padx=5)

        self.load_students()

    def open_bulk_add_window(self):
        """Окно массового добавления списка ФИО для всего класса."""
        win = tk.Toplevel(self.root)
        win.title(f"Добавление списка учеников в {self.current_class} класс")
        win.geometry("420x350")

        tk.Label(win, text="Введите список ФИО учеников (каждый с новой строки):", font=("Arial", 10, "bold")).pack(pady=8)
        text_box = tk.Text(win, width=45, height=14)
        text_box.pack(padx=10, pady=5)

        def save_list():
            raw_text = text_box.get("1.0", tk.END)
            names = [line.strip() for line in raw_text.splitlines() if line.strip()]
            if not names:
                messagebox.showwarning("Внимание", "Список пуст!", parent=win)
                return
            self.db.add_students_bulk(names, self.current_class)
            win.destroy()
            self.load_students()
            messagebox.showinfo("Успешно", f"Добавлено учеников: {len(names)} (отсортированы по алфавиту)")

        tk.Button(win, text="Сохранить весь список", bg="#2e7d32", fg="white", command=save_list).pack(pady=10)

    def load_students(self):
        self.tree.tag_configure("excellent", background="#dcedc8")
        self.tree.tag_configure("good", background="#e1f5fe")
        self.tree.tag_configure("satisfactory", background="#fff9c4")
        self.tree.tag_configure("bad", background="#ffcdd2")
        self.tree.tag_configure("empty", background="#ffffff")

        for row in self.tree.get_children():
            self.tree.delete(row)

        query = self.search_entry.get().strip().lower()
        students = self.db.get_students_by_class(self.current_class)
        for index, st in enumerate(students, start=1):
            st_id, name, cls, grades, absences = st
            if query and query not in name.lower():
                continue
            avg = calculate_average(grades)
            status = get_status(avg)

            if avg == 0:
                tag = "empty"
            elif avg >= 8.5:
                tag = "excellent"
            elif avg >= 6.5:
                tag = "good"
            elif avg >= 4.0:
                tag = "satisfactory"
            else:
                tag = "bad"

            self.tree.insert("", "end", values=(st_id, index, name, grades, avg, status, absences), tags=(tag,))

    def add_student(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Внимание", "Введите ФИО ученика!")
            return
        self.db.add_student(name, self.current_class)
        self.name_entry.delete(0, tk.END)
        self.load_students()

    def get_selected_students(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Подсказка", "Выберите одного или нескольких учеников в таблице!")
            return []
        return [self.tree.item(item)["values"] for item in selected]

    def add_grade(self):
        students = self.get_selected_students()
        if not students:
            return
        grade_text = self.grade_entry.get().strip()
        if not validate_grade(grade_text):
            messagebox.showerror("Ошибка ввода", "Балл должен быть числом от 1 до 10!")
            return

        for student in students:
            st_id, _, _, old_grades, _, _, absences = student
            old_grades_str = str(old_grades) if old_grades else ""
            new_grades = f"{old_grades_str}, {grade_text}".strip(", ")
            self.db.update_student_data(st_id, new_grades, absences)

        self.grade_entry.delete(0, tk.END)
        self.load_students()

    def add_absence(self):
        students = self.get_selected_students()
        if not students:
            return
        for student in students:
            st_id, _, _, grades, _, _, absences = student
            grades_str = str(grades) if grades else ""
            self.db.update_student_data(st_id, grades_str, int(absences) + 1)
        self.load_students()

    def delete_student(self):
        students = self.get_selected_students()
        if not students:
            return
        for student in students:
            self.db.delete_student(student[0])
        self.load_students()

    def clear_quarter(self):
        answer = messagebox.askyesno(
            "Новая четверть",
            f"Вы уверены, что хотите очистить все оценки и пропуски у {self.current_class} класса?\nСписок учеников сохранится."
        )
        if answer:
            self.db.clear_quarter_for_class(self.current_class)
            self.load_students()
            messagebox.showinfo("Готово", "Журнал очищен для новой четверти!")

    def export_json(self):
        students = self.db.get_students_by_class(self.current_class)
        if not students:
            messagebox.showwarning("Внимание", "В этом классе пока нет учеников для экспорта!")
            return

        filepath = filedialog.asksaveasfilename(
            title="Сохранить ведомость класса в JSON",
            defaultextension=".json",
            initialfile=f"vedomost_{self.current_class}.json",
            filetypes=[("JSON файлы", "*.json"), ("Все файлы", "*.*")]
        )
        if not filepath:
            return

        export_to_json(students, filepath)
        messagebox.showinfo("Успешно", f"Ведомость {self.current_class} класса сохранена:\n{filepath}")
        self.root.lift()

    def export_excel(self):
        students = self.db.get_students_by_class(self.current_class)
        if not students:
            messagebox.showwarning("Внимание", "В этом классе пока нет учеников для экспорта!")
            return

        filepath = filedialog.asksaveasfilename(
            title="Сохранить ведомость для Excel",
            defaultextension=".csv",
            initialfile=f"vedomost_{self.current_class}.csv",
            filetypes=[("Таблица Excel (CSV)", "*.csv"), ("Все файлы", "*.*")]
        )
        if not filepath:
            return

        export_to_excel_csv(students, filepath)
        messagebox.showinfo("Успешно", f"Таблица для Excel сохранена:\n{filepath}")
        self.root.lift()


if __name__ == "__main__":
    root = tk.Tk()
    app = ElectronicJournalApp(root)
    root.mainloop()