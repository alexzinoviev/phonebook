import json
import csv
import configparser

contacts = {}

class Controller:
    def read_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        file_type = config['DEFAULT']['file_type']
        return file_type

    def read_from_file(self):
        file_type = self.read_config(self)
        if file_type == 'json':
            return JSONFile.read_from_file(JSONFile)
        elif file_type == 'csv':
            return CSVFile.read_from_file(CSVFile)

    def save_into_file(self, name):
        file_type = self.read_config(self)
        if file_type == 'json':
            JSONFile.save_into_file(JSONFile, name)
        elif file_type == 'csv':
            CSVFile.save_into_file(CSVFile, name)

    def choose_operation(self):
        execute = False
        OPERATIONS = {'C': Operations.create_contact, 'R': Operations.display_results,
                      'U': Operations.update_contact, 'D': Operations.delete_contact, 'Q': quit}
        while True:
            operation = Operations.input_values(self, "Enter operation type: ")
            for oper in OPERATIONS:
                if operation == oper:
                    execute = OPERATIONS[oper]
                    execute(self)
            if execute == False:
                print(operation, "is unsupported operation. Please choose operation from C R U D")


class CSVFile(Controller):
    def save_into_file(self, name):
        with open('f.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in contacts.items():
                writer.writerow([key, value])

    def read_from_file(self):
        try:
            with open('f.csv', 'rt') as csv_file:
                reader = csv.reader(csv_file)
                return dict(reader)
        except FileNotFoundError:
            print("Oops, file is absent")
            return {}


class JSONFile(Controller):
    def save_into_file(self, name):
        with open('f.json', 'wt') as json_file:
            json.dump(contacts, json_file)

    def read_from_file(self):
        try:
            with open('f.json', 'rt') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Oops, file is absent")
            return {}


class Operations:
    def input_values(self, param):
        return input(param)

    def input_name(self):
        return Operations.input_values(self, "Please enter Name: ")

    def input_phone(self):
        return Operations.input_values(self, "Please enter Phone: ")

    def check_contact(self):
        name = Operations.input_name(self)
        if name in contacts:
            phone_exist = True
            return name, phone_exist
        else:
            phone_exist = False
            print("This contact is absent in Phone Book")
            return name, phone_exist

    def create_contact(self):
        name, phone_exist = Operations.check_contact(self)
        if phone_exist == False:
            phone = Operations.input_phone(self)
            contacts[name] = phone
            Controller.save_into_file(self, name)
            print("Contact", name, "with phone:", phone, "created in phone book")
        elif phone_exist == True:
            print("Contact with the same name can't be created")

    def read_contact(self):
        name, phone_exist = Operations.check_contact(self)
        if phone_exist == True:
            return name, contacts[name]

    def update_contact(self):
        name, phone_exist = Operations.check_contact(self)
        if phone_exist == True:
            phone = Operations.input_phone(self)
            contacts[name] = phone
            Controller.save_into_file(self, name)
            print("Contact", name, "has been updated with phone:", phone)

    def delete_contact(self):
        name, phone_exist = Operations.check_contact(self)
        if phone_exist == True:
            contacts.pop(name)
            Controller.save_into_file(self, name)
            print("Contact with name ", name, " has been removed")

    def display_results(self):
        print(Operations.read_contact(self))


if __name__ == '__main__':
    contacts = Controller.read_from_file(Controller)
    Controller.choose_operation(Controller)