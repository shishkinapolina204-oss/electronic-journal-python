import json
from logic import calculate_average, get_status
import csv


def export_to_json(students_data, filename="vedomost_export.json"):
    """Экспортирует данные журнала в структурированный JSON-файл."""
    export_list = []
    for st in students_data:
        st_id, name, cls, grades, absences = st
        avg = calculate_average(grades)
        export_list.append({
            "id": st_id,
            "full_name": name,
            "class": cls,
            "grades": grades,
            "average_score": avg,
            "status": get_status(avg),
            "absences": absences
        })

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(export_list, file, ensure_ascii=False, indent=4)
    return filename



def export_to_excel_csv(students_data, filename="vedomost_export.csv"):
    """Экспортирует данные журнала в таблицу CSV для открытия в Excel."""
    with open(filename, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["№", "ФИО ученика", "Класс", "Оценки", "Средний балл", "Статус", "Пропуски (ч.)"])
        for index, st in enumerate(students_data, start=1):
            st_id, name, cls, grades, absences = st
            avg = calculate_average(grades)
            status = get_status(avg)
            writer.writerow([index, name, cls, grades, avg, status, absences])
    return filename