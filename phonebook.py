import json
import csv
import configparser


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

class Operations():
    def input_values(self, param):
        return input(param)

    def input_name(self):
        return self.input_values("Please enter Name: ")

    def input_phone(self):
        while True:
            phone = self.input_values("Please enter Phone: ")
            try:
                int(phone)
                if len(phone) == 10:
                    return phone
                else:
                    print("Length of the phone must be 10 symbols")
            except ValueError:
                print("Phone number should be numeric")

    def check_contact(self):
        name = self.input_name()
        if name in contacts:
            phone_exist = True
            return name, phone_exist
        else:
            phone_exist = False
            print("This contact is absent in Phone Book")
            return name, phone_exist

    def create_contact(self):
        name, phone_exist = self.check_contact()
        if phone_exist is False:
            phone = self.input_phone()
            contacts[name] = phone
            Controller.save_into_file(self, name)
            print("Contact", name, "with phone:", phone, "created in phone book")
        else:
            print("Contact with the same name can't be created")

    def read_contact(self):
        name, phone_exist = self.check_contact()
        if phone_exist is True:
            return name, contacts[name]

    def update_contact(self):
        name, phone_exist = self.check_contact()
        if phone_exist is True:
            phone = self.input_phone()
            contacts[name] = phone
            Controller.save_into_file(self, name)
            print("Contact", name, "has been updated with phone:", phone)

    def delete_contact(self):
        name, phone_exist = self.check_contact()
        if phone_exist is True:
            contacts.pop(name)
            Controller.save_into_file(self, name)
            print("Contact with name ", name, " has been removed")

    def display_results(self):
        print(self.read_contact())


class Controller(JSONFile, CSVFile, Operations):
    def read_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        file_type = config['DEFAULT']['file_type']
        return file_type

    def read_from_file(self):
        file_type = self.read_config()
        if file_type == 'json':
            return JSONFile.read_from_file(self)
        elif file_type == 'csv':
            return CSVFile.read_from_file(self)

    def save_into_file(self, name):
        file_type = self.read_config()
        if file_type == 'json':
            JSONFile.save_into_file(self, name)
        elif file_type == 'csv':
            CSVFile.save_into_file(self, name)

    def choose_operation(self):
        execute = False
        possible_operations = {'C': Operations.create_contact, 'R': Operations.display_results,
                               'U': Operations.update_contact, 'D': Operations.delete_contact, 'Q': quit}
        while True:
            chosen_operation = Operations.input_values(self, "Enter operation type: ")
            for operation in possible_operations:
                if chosen_operation == operation:
                    execute = possible_operations[operation]
                    execute(self)
            if execute == False:
                print(chosen_operation, "is unsupported operation. Please choose operation from C R U D")


if __name__ == '__main__':
    json_file = JSONFile()
    csv_file = CSVFile()
    controller = Controller()
    operations = Operations()
    contacts = controller.read_from_file()
    controller.choose_operation()
