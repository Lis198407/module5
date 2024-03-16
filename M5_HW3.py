"""
Вимоги до завдання:
+Скрипт повинен приймати шлях до файлу логів як аргумент командного рядка.
+Скрипт повинен приймати не обов'язковий аргумент командного рядка, після аргументу шляху до файлу логів. 
Він відповідає за виведення всіх записи певного рівня логування. 
І приймає значення відповідно до рівня логування файлу. Наприклад аргумент error виведе всі записи рівня ERROR з файлу логів.
Скрипт має зчитувати і аналізувати лог-файл, підраховуючи кількість записів для кожного рівня логування (INFO, ERROR, DEBUG, WARNING).
+ Реалізуйте функцію parse_log_line(line: str) -> dict для парсингу рядків логу.
+ Реалізуйте функцію load_logs(file_path: str) -> list для завантаження логів з файлу.
+Реалізуйте функцію filter_logs_by_level(logs: list, level: str) -> list для фільтрації логів за рівнем.
+Реалізуйте функцію count_logs_by_level(logs: list) -> dict для підрахунку записів за рівнем логування.
+Результати мають бути представлені у вигляді таблиці з кількістю записів для кожного рівня. 
+Для цього реалізуйте функцію display_log_counts(counts: dict), яка форматує та виводить результати. 
Вона приймає результати виконання функції count_logs_by_level.

Рекомендації для виконання:
Перш ніж почати, ознайомтеся зі структурою вашого лог-файлу. Зверніть увагу на формат дати та часу, 
    рівні логування INFO, ERROR, DEBUG, WARNING і структуру повідомлень.
Зрозумійте, як розділені різні компоненти логу, це зазвичай пробіли або спеціальні символи.
Розділіть ваше завдання на логічні блоки і функції для кращої читабельності і подальшого розширення.
+Парсинг рядка логу виконує ****функцію parse_log_line(line: str) -> dict, 
+    яка приймає рядок з логу як вхідний параметр і повертає словник з розібраними компонентами: дата, час, рівень, повідомлення. 
+    Використовуйте методи рядків, такі як split(), для розділення рядка на частини.
+ Завантаження лог-файлів виконує функція load_logs(file_path: str) -> list, що відкриває файл, 
+    читає кожен рядок і застосовує на нього функцію parse_log_line, зберігаючи результати в список.
+ Фільтрацію за рівнем логування виконує функція filter_logs_by_level(logs: list, level: str) -> list. 
+    Вона дозволить вам отримати всі записи логу для певного рівня логування.
+Підрахунок записів за рівнем логування повинна робити функція count_logs_by_level(logs: list) -> dict, 
    яка проходить по всім записам і підраховує кількість записів для кожного рівня логування.
Вивід результатів виконайте за допомоги функції display_log_counts(counts: dict), 
    яка форматує та виводить результати підрахунку в читабельній формі.
Ваш скрипт повинен вміти обробляти різні види помилок, такі як відсутність файлу або помилки при його читанні. 
Використовуйте блоки try/except для обробки виняткових ситуацій.

Критерії оцінювання:
Скрипт виконує всі зазначені вимоги, правильно аналізуючи лог-файли та виводячи інформацію.
Скрипт коректно обробляє помилки, такі як неправильний формат лог-файлу або відсутність файлу.
При розробці обов'язково було використано один з елементів функціонального програмування: лямбда-функція, списковий вираз, функція filter, тощо.
Код добре структурований, зрозумілий і містить коментарі там, де це необхідно.

"""
from pathlib import Path
from datetime import datetime

def load_logs(file_path:Path)->list:                              #reads logs from filepath to list of dictionaries

    def parse_log_line(line: str) -> dict:                        #for parsing log line
        try:
            line_list = line.split()
            line_list = [line_list[0],line_list[1],line_list[2]," ".join(line_list[3:])] #creating a list for nedeed detalization
            log_dict = {
                'date':        datetime.strptime(line_list[0],"%Y-%m-%d"),
                'time':        datetime.strptime(line_list[1],"%H:%M:%S"),
                'LOGTYPE':     line_list[2],
                'description': line_list[3]
            }
            return log_dict
        except Exception as ex:
            print(f"error in parse_log_line: {ex}, line: {line}")
            return None

    try:
        log_list=[]
        log_dict={}
        with open(file_path, "r") as file: #, encoding="utf-8"    # reading log from file
            for line in file:
                log_dict = parse_log_line(line)
                log_list.append(log_dict)
        return log_list
    except FileNotFoundError as ex:
        print(f"error in load_logs: {ex}")
        return None
    

def filter_logs_by_level(logs: list, level: str) -> list:                                         # For filtration log by level
    new_list = [x for x in logs if x["LOGTYPE"] == level]
    return new_list

def count_logs_by_level(logs: list) -> dict:                                                      #for counting logs by levels
    try:
        log_types = {log["LOGTYPE"] for log in logs}                                              #set for log levels
        log_dict = {log_type: len(filter_logs_by_level(logs,log_type)) for log_type in log_types} #Dictionary with levels and quantity of records
        return log_dict
    except Exception as ex:   #TypeError
        print(f"Error in count logs by level: {ex}")
        return None

def display_logs_by_level(logs: list, level: str):
    filtered_logs = filter_logs_by_level(logs, level)
    print(f"Logs by level {level}:")
    message_template = "--------------------------------------------------\n   Date    |  Time  |    Log description\n--------------------------------------------------\n"
    format_log = lambda log: f" {log['date'].date()}|{log['time'].time()}|{log['description']}\n"
    messages = map(format_log, filtered_logs)
    message = message_template + ''.join(messages) + "--------------------------------------------------\n"
    print(message)

def display_log_counts(counts: dict):
    symbol = ' '
    if len(counts)>=1:
        message = "Quantity of records in Log file by Log levels:\n --------------------------------\n Log level |   Counts of logs\n --------------------------------\n"
        for key, value in counts.items():
            message += f" {key}{symbol*(10-len(str(key)))}| {value}\n"
        message +="---------------------------------\n"
        print(message)
    else:
        print('no data for output')
    
def main():
    user_input = input(r"Welcome to log-reader! Enter File path to log file in format '-X:\folder\file.txt' or press enter for default: ")
    
    if  len(user_input) == 0:                                                   #Path to File if not entered
        file_path = Path("HW3_log_file.txt")
    else:
        try:
            file_path = Path(user_input)
        except Exception as ex: 
            print(ex)

    logs = load_logs(file_path)                                             #Load logs into list of dictionaries
    if logs is None:
        print("Please try another file or check data structure of file")
    else:
        log_dict = count_logs_by_level(logs)    
        logs_level = input(r"Please enter Log Level for detailed information or press enter for default: ")
        if len(logs_level) == 0:                                            #on default - counting logs by levels, else - detailed info by level
            display_log_counts(log_dict)
        else:
            display_logs_by_level(logs, logs_level)

if __name__ == "__main__":
    main()