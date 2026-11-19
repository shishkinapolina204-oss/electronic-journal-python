def calculate_average(grades_str):
    """Вычисляет средний балл по 10-балльной шкале из строки оценок."""
    if not grades_str or not grades_str.strip():
        return 0.0
    try:
        grades = [int(g.strip()) for g in grades_str.split(",") if g.strip()]
        if not grades:
            return 0.0
        return round(sum(grades) / len(grades), 2)
    except ValueError:
        return 0.0


def validate_grade(grade_text):
    """Проверяет, что балл является целым числом от 1 до 10 (шкала РК)."""
    try:
        grade = int(grade_text)
        return 1 <= grade <= 10
    except ValueError:
        return False


def get_status(avg_score):
    """Определяет уровень успеваемости по 10-балльной системе Казахстана."""
    if avg_score == 0:
        return "Нет оценок"
    elif avg_score >= 8.5:
        return "Отлично (5)"
    elif avg_score >= 6.5:
        return "Хорошо (4)"
    elif avg_score >= 4.0:
        return "Удовл. (3)"
    else:
        return "Неуспевающий (2)"