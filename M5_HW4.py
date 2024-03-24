"""
Вимоги до завдання:
Доробіть консольного бота помічника з попереднього домашнього завдання та додайте обробку помилок за допомоги декораторів.

Вимоги до завдання:
Всі помилки введення користувача повинні оброблятися за допомогою декоратора input_error. 
Цей декоратор відповідає за повернення користувачеві повідомлень типу "Enter user name", "Give me name and phone please" тощо.
Декоратор input_error повинен обробляти винятки, що виникають у функціях - handler і це винятки: 
           KeyError, ValueError, IndexError. Коли відбувається виняток декоратор повинен повертати відповідну відповідь користувачеві. 
Виконання програми при цьому не припиняється.

Критерії оцінювання:
Наявність декоратора input_error, який обробляє помилки введення користувача для всіх команд.
Обробка помилок типу KeyError, ValueError, IndexError у функціях за допомогою декоратора input_error.
Кожна функція для обробки команд має власний декоратор input_error, який обробляє відповідні помилки і повертає відповідні повідомлення про помилку.
Коректна реакція бота на різні команди та обробка помилок введення без завершення програми.
"""

from functools import wraps
from pathlib import Path
import math

def file_error(func):                                                             #decorator for Open-Save database in file
    @wraps(func)
    def inner(*args, **kwargs):
        try:  
            phones_list = []
            phones_list = func(*args)
            print("Phones list imported/saved successfully")
            return phones_list
        except FileNotFoundError as ex:
            print(f"Error while importing/saving data. Please check Path and File. Error: {ex}")
    return inner

@file_error
def get_phones_info(file_path:Path)->list:                                          #reads names and phones from file to list of dictionary
    user_dict= {}
    phones_list=[]
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:                            
            try:
                line = line.strip()
                user_str = line.split(",")
                user_dict = {
                    'name': user_str[0],
                    'phone': user_str[1].strip()
                    }
                phones_list.append(user_dict)
            except Exception as ex:
                print(f"mistake in data structure: {ex}, line: {line}")
    return phones_list

@file_error
def save_to_file(phones_info:list, file_path:Path):                                    #writes database to file
    with open(file_path, "w", encoding="utf-8") as file:
        for dictionary in phones_info:
            file.write(f"{dictionary.get("name")},{dictionary.get("phone")}\n")

def input_error(func):                                                                #decorator for main chat-bot functions
    @wraps(func)
    def inner(*args):
        phone_list=[]
        name=''
        phone=''
        try:                                                                          #parsing arguments from command promt to variables
            if func.__name__ == 'parse_input':
                user_input = args[0]
            else:
                phone_list = args[0]
                name = args[1][0]
                phone = args[1][1]
        except (IndexError, ValueError, TypeError):
            pass                                                                      #in case of mistake doing nothing. all checks will be in block Match
        
        match func.__name__:                                                          #for different function differenet input arguments and feedback for user 
            case "add_contact":
                try:
                   return func(phone_list, name, phone)
                except Exception as ex:
                    print(f"Unable to add contact. Error: {ex}")
            case "change_contact":                                                    #for different function - differenet messages and bot function calls
                try:
                    return func(phone_list, name, phone)
                except Exception as ex:
                    print(f"Unable to change contact. No such Name or mistake in data structure. Error: {ex}")
            case "show_phone":
                try:
                    return func(phone_list, name)
                except Exception as ex:
                    print(f"Unable to show phone number. Error: {ex}")
            case "show_all":
                try:
                    return func(phone_list)
                except Exception as ex:
                    print(f"Unable to show all database. Error: {ex}")
            case "parse_input":
                try:
                    return func(*args)
                except Exception as ex:
                    print(f"Unable to parse parameters from command prompt. please use 'help' for help. Error: {ex}")
            case _:
                print("no such function")
    return inner

def find_dictionary_by_name(phone_info:list, target_name:str):                   #finds entry in list by name
    for dictionary in phone_info:
        if "name" in dictionary and dictionary["name"] == target_name:
            return dictionary                                                     #Return dictionary with name = target_name
    return None                                                                   #Return None if the name is not found in any dictionary

@input_error
def add_contact(phones_info:list,name_to_add:str,phone_to_add:str)->str:          #adds new line: name and phone to the list of dictionaries
    phones_info.append({"name": name_to_add, "phone": phone_to_add})
    return "data added"

@input_error
def change_contact(phones_info:list,name_to_change:str,new_phone:str)->str:       #change phone by name
    dict_to_change = {}
    dict_to_change = find_dictionary_by_name(phones_info,name_to_change)
    if dict_to_change != None:
        dict_to_change.update({'name': name_to_change, 'phone': new_phone})
        message = f"data updated! name:{dict_to_change.get("name")}, phone:{dict_to_change.get("phone")}"
    else:    
        message = None
    return message

@input_error
def show_phone(phones_info:list, name_to_find:str)->str:                         #shows phone by name
    dict_to_find = find_dictionary_by_name(phones_info,name_to_find)
    if dict_to_find != None:
        message = f"Phone number of {dict_to_find.get("name")} is {dict_to_find.get("phone")}"
    else:    
        message = None
    return message

@input_error
def show_all(phones_info:list)->str:                                             #shows all contacts
    symbol = " "
    i = 1
    if len(phones_info)>=1:
        message = "№  |          name          |         phone\n -------------------------------------------------\n"
        for line in phones_info:
            move_name = math.trunc(12-len(line["name"])/2)                       #formating data entries for output from a list
            move_name_right = move_name if (len(line["name"]) % 2) == 0  else move_name+1
            move_phone = math.trunc(12-len(line["phone"])/2)
            message += f" {i}{symbol*math.trunc(3-len(str(i))/2)}|{symbol*move_name}{line["name"]}{symbol*(move_name_right)}|{symbol*move_phone}{line["phone"]}\n"
            i+=1
    else: 
        message = None
    return message

@input_error
def parse_input(user_input):                                                    #parsed input. !! all arguments should start from "-"
    cmd, *args = user_input.split('-')
    cmd = cmd.strip().lower()
    args = [arg.strip() for arg in args]                                        # Strip spaces from each argument
    return cmd, args

def main():
    file_path = Path("phones.txt")
    phones_info = []
    print("Welcome to the assistant bot!")
    while True:                                                                # execution of commands to bot
        message = ""
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)                                #parsing command promt in format <command> <-argumument1> <-argument2>...
        command = command.lower()
       
        match command:                                                         # case for bot commands
            case "close"|"exit":
                print("Good bye!")
                break
            case "hello":                   print("How can I help you? print 'help' for all commands")
            case "get from file"|"get":     phones_info = get_phones_info(file_path)
            case "add"|"add contact":       print(add_contact(phones_info, args))
            case "change contact"|"change": print(change_contact(phones_info, args))
            case "show contacts"|"all":     print(f"Your contact database: \n {show_all(phones_info)}")
            case "show phone"|"phone":      print(show_phone(phones_info, args))
            case "save to file"|"save":     save_to_file(phones_info,file_path)
            case "help"|"?"|"/?":
                print("""available command of bot is:  
                      "hello" - to say hello to bot   
                      "close" or "exit" - to stop bot
                      commands for contacts: 
                          "get from file" or "get" - import contacts from file
                          "add contact" or "add" with arguments "-Name" and "-Phone" will add contact to database (DB). for example add -NewName -NewPhone
                          "change contact" or "change" with arguments "-Name" and "-Phone" will change contact in DB
                          "show contacts" or "all" - to show all contacts in DB
                          "show phone" or "phone" - with argument "-Name" will show the phone of contact
                          "save to file" or "save" - save names and phones to file
                    """)
            case _:                
                print("Invalid command. if you need assistance please enter: help")

if __name__ == "__main__":
    main()