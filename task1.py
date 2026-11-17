#Варіант 48. Фінанси виробничих дільниць
#Завдання 1. Чистий результат після фіксованої плати
import json
import re
from dataclasses import dataclass
from functools import wraps


@dataclass
class Record:
    code: str
    group: str
    x: int
    y: int

#декоратор, який для кожної функції створює свою незалежну обгортку з лічильником викликів
def count_calls(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1#лічильник росте навіть якщо буде виняток
        return function(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


@count_calls
def evaluate(record: Record) -> int:
    return record.x - record.y - 8#плата 8 грн за умовою


def read_result(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    evaluate.calls = 0#кожен запуск починається з нуля
    try:
        input_filename = input().replace('\r', '').strip()
        output_filename = input().replace('\r', '').strip()
        t_input = input().replace('\r', '').strip()
    except EOFError:
        print("Статус: FORMAT_ERROR")
        print("Функція: evaluate")
        print("Виклики: 0")
        print("Збережено: -")
        print("JSON: -")
        return
    #Перевірка назв файлів та порогу T
    filename_pattern = re.compile(r'^[a-z][a-z0-9_\.]{0,39}$')
    if not filename_pattern.match(input_filename) or not filename_pattern.match(output_filename):
        print("Статус: FORMAT_ERROR")
        print("Функція: evaluate")
        print("Виклики: 0")
        print("Збережено: -")
        print("JSON: -")
        return

    if input_filename == output_filename:
        print("Статус: FORMAT_ERROR")
        print("Функція: evaluate")
        print("Виклики: 0")
        print("Збережено: -")
        print("JSON: -")
        return

    try:
        T = int(t_input)
    except ValueError:
        print("Статус: FORMAT_ERROR")
        print("Функція: evaluate")
        print("Виклики: 0")
        print("Збережено: -")
        print("JSON: -")
        return

    if not (0 <= T <= 1000000):
        print("Статус: FORMAT_ERROR")
        print("Функція: evaluate")
        print("Виклики: 0")
        print("Збережено: -")
        print("JSON: -")
        return

    #Перевірка наявності вхідного файлу
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("Статус: FILE_MISSING")
        print("Функція: evaluate")
        print("Виклики: 0")
        print("Збережено: -")
        print("JSON: -")
        return
    except Exception:
        print("Статус: FORMAT_ERROR")
        print("Функція: evaluate")
        print("Виклики: 0")
        print("Збережено: -")
        print("JSON: -")
        return

    #Перевірка синтаксису JSON (порожній файл або тільки пробіли теж дадуть помилку)
    try:
        data = json.loads(content)
    except Exception:
        print("Статус: FORMAT_ERROR")
        print("Функція: evaluate")
        print("Виклики: 0")
        print("Збережено: -")
        print("JSON: -")
        return

    if not isinstance(data, list):
        print("Статус: DATA_ERROR")
        print("Функція: evaluate")
        print("Виклики: 0")
        print("Збережено: -")
        print("JSON: -")
        return

    if len(data) > 100:
        print("Статус: DATA_ERROR")
        print("Функція: evaluate")
        print("Виклики: 0")
        print("Збережено: -")
        print("JSON: -")
        return

    code_pattern = re.compile(r'^[A-Z][A-Z0-9_]{0,11}$')
    seen_codes = set()
    records = []

    #Строга перевірка вмісту масиву (через isinstance перевіряємо тип значення: dict, str, int, а bool окремо, бо в Python він теж int)
    for item in data:
        if not isinstance(item, dict):
            print("Статус: DATA_ERROR")
            print("Функція: evaluate")
            print("Виклики: 0")
            print("Збережено: -")
            print("JSON: -")
            return

        keys = list(item.keys())
        if sorted(keys) != sorted(["code", "group", "x", "y"]):
            print("Статус: DATA_ERROR")
            print("Функція: evaluate")
            print("Виклики: 0")
            print("Збережено: -")
            print("JSON: -")
            return

        code = item["code"]
        group = item["group"]
        x = item["x"]
        y = item["y"]

        if not isinstance(code, str) or not code_pattern.match(code):
            print("Статус: DATA_ERROR")
            print("Функція: evaluate")
            print("Виклики: 0")
            print("Збережено: -")
            print("JSON: -")
            return

        if not isinstance(group, str) or not code_pattern.match(group):
            print("Статус: DATA_ERROR")
            print("Функція: evaluate")
            print("Виклики: 0")
            print("Збережено: -")
            print("JSON: -")
            return

        if not isinstance(x, int) or isinstance(x, bool):
            print("Статус: DATA_ERROR")
            print("Функція: evaluate")
            print("Виклики: 0")
            print("Збережено: -")
            print("JSON: -")
            return

        if not isinstance(y, int) or isinstance(y, bool):
            print("Статус: DATA_ERROR")
            print("Функція: evaluate")
            print("Виклики: 0")
            print("Збережено: -")
            print("JSON: -")
            return

        if not (0 <= x <= 10000) or not (0 <= y <= 10000):
            print("Статус: DATA_ERROR")
            print("Функція: evaluate")
            print("Виклики: 0")
            print("Збережено: -")
            print("JSON: -")
            return

        if code in seen_codes:
            print("Статус: DATA_ERROR")
            print("Функція: evaluate")
            print("Виклики: 0")
            print("Збережено: -")
            print("JSON: -")
            return

        seen_codes.add(code)
        records.append(Record(code=code, group=group, x=x, y=y))

    #Обробка та обчислення (evaluate викликається один раз для кожного запису, навіть якщо він не пройде відбір)
    items_result = []
    groups_aggregated = {}

    for rec in records:
        val = evaluate(rec)
        if val >= T:#рівність порогу включається
            items_result.append({
                "code": rec.code,
                "group": rec.group,
                "x": rec.x,
                "y": rec.y,
                "value": val
            })
            if rec.group not in groups_aggregated:
                groups_aggregated[rec.group] = {"count": 1, "total": val, "min": val, "max": val}
            else:
                groups_aggregated[rec.group]["count"] += 1
                groups_aggregated[rec.group]["total"] += val
                if val < groups_aggregated[rec.group]["min"]:
                    groups_aggregated[rec.group]["min"] = val
                if val > groups_aggregated[rec.group]["max"]:
                    groups_aggregated[rec.group]["max"] = val

    #Сортування за спаданням value потім за зростанням code
    items_result.sort(key=lambda i: (-i["value"], i["code"]))

    #Формування groups списку
    groups_list = []
    for g_name, data_g in groups_aggregated.items():
        groups_list.append({
            "group": g_name,
            "count": data_g["count"],
            "total": data_g["total"],
            "min": data_g["min"],
            "max": data_g["max"]
        })

    #Сортування за зростанням total потім за спаданням count і потім за зростанням group
    groups_list.sort(key=lambda g: (g["total"], -g["count"], g["group"]))

    total_sum = sum(item["value"] for item in items_result)
    total_count = len(items_result)

    final_dict = {
        "items": items_result,
        "groups": groups_list,
        "count": total_count,
        "total": total_sum
    }

    #Збереження у файл у компактному вигляді
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(final_dict, f, separators=(',', ':'), ensure_ascii=False)
    except Exception:
        print("Статус: FORMAT_ERROR")
        print("Функція: evaluate")
        print("Виклики: 0")
        print("Збережено: -")
        print("JSON: -")
        return

    #Повторне читання через read_result для виведення
    try:
        verified_dict = read_result(output_filename)
        compact_json = json.dumps(verified_dict, separators=(',', ':'), ensure_ascii=False)
    except Exception:
        print("Статус: FORMAT_ERROR")
        print("Функція: evaluate")
        print("Виклики: 0")
        print("Збережено: -")
        print("JSON: -")
        return

    print("Статус: OK")
    print("Функція: evaluate")
    print(f"Виклики: {evaluate.calls}")
    print(f"Збережено: {output_filename}")
    print(f"JSON: {compact_json}")


if __name__ == '__main__':
    main()