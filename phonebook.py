import json, csv, configparser

def input_values(param):
    return input(param)


def input_name():
    return input_values("Please enter Name: ")


def input_phone():
    return input_values("Please enter Phone: ")


def check_contact():
    name = input_name()
    if name in contacts:
        phone_exist = True
        return name, phone_exist
    else:
        phone_exist = False
        print("This contact is absent in Phone Book")
        return name, phone_exist


def create_contact():
    name, phone_exist = check_contact()
    if phone_exist == False:
        phone = input_phone()
        contacts[name] = phone
        save_into_file(name)
        print("Contact", name, "with phone:", phone, "created in phone book")
    elif phone_exist == True:
        print("Contact with the same name can't be created")


def read_contact():
    name, phone_exist = check_contact()
    if phone_exist == True:
        return name, contacts[name]


def update_contact():
    name, phone_exist = check_contact()
    if phone_exist == True:
        phone = input_phone()
        contacts[name] = phone
        save_into_file(name)
        print("Contact", name, "has been updated with phone:", phone)


def delete_contact():
    name, phone_exist = check_contact()
    if phone_exist == True:
        contacts.pop(name)
        save_into_file(name)
        print("Contact with name ", name, " has been removed")


def display_results(param):
    if param !=None:
        print(param)


def choose_operation():
    while True:
        operation = input_values("Enter operation type: ")
        if operation == "C":
            create_contact()
        elif operation == "R":
            display_results(read_contact())
        elif operation == "U":
            update_contact()
        elif operation == 'D':
            delete_contact()
        elif operation == 'Q':
            quit()
        else:
            print(operation, "is unsupported operation. Please choose operation from C R U D")
            continue


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    file_type = config['DEFAULT']['file_type']
    return file_type


def save_into_file(name):
    file_type = read_config()
    if file_type == 'json':
        with open('f.json', 'wt') as json_file:
            json.dump(contacts, json_file)
    elif file_type == 'csv':
        with open('f.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in contacts.items():
                writer.writerow([key, value])


def read_from_file():
    file_type = read_config()
    try:
        if file_type == 'json':
            with open('f.json', 'rt') as file:
                return json.load(file)
        elif file_type == 'csv':
            with open('f.csv', 'rt') as csv_file:
                reader = csv.reader(csv_file)
                contacts = dict(reader)
                return contacts
    except FileNotFoundError:
        print("Oops, file is absent")
        return {}


# def read_from_file_csv():
#     try:
#         with open('f.csv', 'rt') as csv_file:
#             reader = csv.reader(csv_file)
#             contacts = dict(reader)
#             return contacts
#     except FileNotFoundError:
#         print("Oops, file is absent")
#         return {}


contacts = read_from_file()
choose_operation()


w = csv.writer(f)
#     w.writerow(('aa aa', 1234))
