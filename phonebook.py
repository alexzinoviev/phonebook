import json, csv

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


def save_into_file(name):
    with open('f.json', 'wt') as json_file:
        json.dump(contacts, json_file)
    with open('f.csv', 'wt') as csv_file:
        w = csv.writer(csv_file)
        w.writerow({contacts[name],name})


def read_from_file():
    try:
        with open('f.json', 'rt') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Oops, file is absent")
        return {}



contacts = read_from_file()
choose_operation()


w = csv.writer(f)
#     w.writerow(('aa aa', 1234))
