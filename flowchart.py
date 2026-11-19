import tkinter as tk

root = tk.Tk()
root.title("Блок-схема алгоритма ПО «Электронный журнал» (ГОСТ 19.701-90)")
root.configure(bg="white")

canvas = tk.Canvas(root, width=760, height=650, bg="white", highlightthickness=0)
canvas.pack(padx=5, pady=5)

FONT_TITLE = ("Arial", 10, "bold")
FONT_TEXT = ("Arial", 8)
FONT_BOLD = ("Arial", 8, "bold")


def draw_oval(x, y, w, h, text):
    canvas.create_oval(x - w/2, y - h/2, x + w/2, y + h/2, fill="#e3f2fd", outline="#1565c0", width=1.8)
    canvas.create_text(x, y, text=text, font=FONT_BOLD, fill="#0d47a1", justify="center")


def draw_rect(x, y, w, h, text):
    canvas.create_rectangle(x - w/2, y - h/2, x + w/2, y + h/2, fill="#ffffff", outline="#263238", width=1.8)
    canvas.create_text(x, y, text=text, font=FONT_TEXT, fill="#212121", justify="center")


def draw_io(x, y, w, h, text):
    skew = 12
    pts = [x - w/2 + skew, y - h/2, x + w/2 + skew, y - h/2,
           x + w/2 - skew, y + h/2, x - w/2 - skew, y + h/2]
    canvas.create_polygon(pts, fill="#fffde7", outline="#f57f17", width=1.8)
    canvas.create_text(x, y, text=text, font=FONT_TEXT, fill="#212121", justify="center")


def draw_rhombus(x, y, w, h, text):
    pts = [x, y - h/2, x + w/2, y, x, y + h/2, x - w/2, y]
    canvas.create_polygon(pts, fill="#e8f5e9", outline="#2e7d32", width=1.8)
    canvas.create_text(x, y, text=text, font=FONT_BOLD, fill="#1b5e20", justify="center")


def arrow(x1, y1, x2, y2):
    canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="#37474f", width=1.6)


canvas.create_text(380, 16, text="Блок-схема основного алгоритма ПО «Электронный журнал» (ГОСТ 19.701-90)", font=FONT_TITLE, fill="#1a237e")

cx = 290
draw_oval(cx, 48, 160, 32, "Начало")
arrow(cx, 64, cx, 82)

draw_rect(cx, 102, 270, 40, "Подключение к БД SQLite\n(school_journal.db)")
arrow(cx, 122, cx, 140)

draw_io(cx, 160, 270, 40, "Ввод логина и пароля учителя")
arrow(cx, 180, cx, 198)

draw_rhombus(cx, 230, 240, 64, "Логин и пароль\nверны?")

# Ветка Нет (Авторизация)
canvas.create_line(cx + 120, 230, 590, 230, fill="#c62828", width=1.6)
canvas.create_text(445, 220, text="Нет", font=FONT_BOLD, fill="#c62828")
canvas.create_line(590, 230, 590, 202, fill="#c62828", width=1.6)
draw_rect(590, 182, 160, 40, "Сообщение об ошибке\nдоступа")
canvas.create_line(590, 162, 590, 158, fill="#c62828", width=1.6)
arrow(590, 158, cx + 141, 158)

# Ветка Да (Авторизация)
canvas.create_text(cx + 16, 270, text="Да", font=FONT_BOLD, fill="#2e7d32")
arrow(cx, 262, cx, 282)

draw_io(cx, 304, 290, 44, "Выбор / создание класса и загрузка\nсписка учеников по алфавиту")
arrow(cx, 326, cx, 344)

draw_io(cx, 366, 290, 44, "Выбор ученика(ов) и ввод\nформативного балла (1–10)")
arrow(cx, 388, cx, 406)

draw_rhombus(cx, 438, 240, 64, "Балл в диапазоне\nот 1 до 10?")

# Ветка Нет (Валидация)
canvas.create_line(cx + 120, 438, 590, 438, fill="#c62828", width=1.6)
canvas.create_text(445, 428, text="Нет", font=FONT_BOLD, fill="#c62828")
canvas.create_line(590, 438, 590, 410, fill="#c62828", width=1.6)
draw_rect(590, 390, 160, 40, "Ошибка валидации\nввода балла")
canvas.create_line(590, 370, 590, 366, fill="#c62828", width=1.6)
arrow(590, 366, cx + 151, 366)

# Ветка Да (Валидация)
canvas.create_text(cx + 16, 478, text="Да", font=FONT_BOLD, fill="#2e7d32")
arrow(cx, 470, cx, 490)

draw_rect(cx, 514, 300, 48, "Сохранение в SQLite, расчёт среднего\nбалла, статуса (РК) и подсветка строки")
arrow(cx, 538, cx, 556)

draw_io(cx, 576, 280, 40, "Экспорт ведомости в JSON / Excel")
arrow(cx, 596, cx, 612)

draw_oval(cx, 628, 160, 32, "Конец")

root.mainloop()