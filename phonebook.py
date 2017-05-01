import json
import csv
import configparser


class Controller:
    def read_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        file_type = config['DEFAULT']['file_type']
        return file_type

    def read_from_file(self):
        file_type = self.read_config()
        if file_type == 'json':
            return json_file.read_from_file()
        elif file_type == 'csv':
            return csv_file.read_from_file()

    def save_into_file(self, name):
        file_type = self.read_config()
        if file_type == 'json':
            json_file.save_into_file(name)
        elif file_type == 'csv':
            csv_file.save_into_file(name)

    def choose_operation(self):
        execute = False
        possible_operations = {'C': operations.create_contact, 'R': operations.display_results,
                               'U': operations.update_contact, 'D': operations.delete_contact, 'Q': quit}
        while True:
            chosen_operation = operations.input_values("Enter operation type: ")
            for operation in possible_operations:
                if chosen_operation == operation:
                    execute = possible_operations[operation]
                    execute()
            if execute == False:
                print(chosen_operation, "is unsupported operation. Please choose operation from C R U D")


class CSVFile:
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


class JSONFile:
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
        return operations.input_values("Please enter Name: ")

    def input_phone(self):
        return operations.input_values("Please enter Phone: ")

    def check_contact(self):
        name = operations.input_name()
        if name in contacts:
            phone_exist = True
            return name, phone_exist
        else:
            phone_exist = False
            print("This contact is absent in Phone Book")
            return name, phone_exist

    def create_contact(self):
        name, phone_exist = operations.check_contact()
        if phone_exist == False:
            phone = operations.input_phone()
            contacts[name] = phone
            controller.save_into_file(name)
            print("Contact", name, "with phone:", phone, "created in phone book")
        elif phone_exist == True:
            print("Contact with the same name can't be created")

    def read_contact(self):
        name, phone_exist = operations.check_contact()
        if phone_exist == True:
            return name, contacts[name]

    def update_contact(self):
        name, phone_exist = operations.check_contact()
        if phone_exist == True:
            phone = operations.input_phone()
            contacts[name] = phone
            controller.save_into_file(name)
            print("Contact", name, "has been updated with phone:", phone)

    def delete_contact(self):
        name, phone_exist = operations.check_contact()
        if phone_exist == True:
            contacts.pop(name)
            controller.save_into_file(name)
            print("Contact with name ", name, " has been removed")

    def display_results(self):
        print(operations.read_contact())


if __name__ == '__main__':
    json_file = JSONFile()
    csv_file = CSVFile()
    controller = Controller()
    operations = Operations()

    contacts = controller.read_from_file()
    print(contacts)
    controller.choose_operation()
