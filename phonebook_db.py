import sqlite3

global contacts
global db

class SQL:
    def __init__(self):
        global db
        db = sqlite3.connect('phonebook.db')


    def after_request(self):
        db.close()


    def read_all_from_db(self):
        cursor = db.cursor()
        contacts = cursor.execute("SELECT name, phone FROM contacts")
        for row in contacts:
            print(row)
        #self.after_request()


    def read_by_name(self, name):
        cursor = db.cursor()
        results = cursor.execute("SELECT name, phone FROM contacts WHERE name = ?", [name])
        contact = results.fetchall()
        if contact == []:
            print('Contact with ' + name + ' not found')
            #self.after_request()
            return None
        else:
            #self.after_request()
            return contact


    def insert_to_table(self, name, phone):
        cursor = db.cursor()
        cursor.execute("INSERT INTO contacts(name, phone) VALUES (?,?)", (name, phone,))
        db.commit()
        #self.after_request()


    def delete_from_db(self, name):
        cursor = db.cursor()
        cursor.execute("DELETE FROM contacts WHERE name = ?", [name])
        db.commit()
        #self.after_request()

    def update_db(self, phone, name):
        cursor = db.cursor()
        cursor.execute("UPDATE contacts SET phone = ? WHERE name = ?", (phone, name))
        db.commit()


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
        sql = SQL()
        name = self.input_name()
        exist = sql.read_by_name(name)
        if exist == None:
            phone_exist = False
            print("This contact is absent in Phone Book")
            return name, phone_exist
        else:
            phone_exist = True
            return name, phone_exist


    def create_contact(self):
        name, phone_exist = self.check_contact()
        if phone_exist is False:
            phone = self.input_phone()
            sql.insert_to_table(name, phone)
            print("Contact", name, "with phone:", phone, "created in phone book")
        else:
            print("Contact with the same name can't be created")

    def read_contact(self):
        name, phone_exist = self.check_contact()
        if phone_exist is True:
            return controller.read_by_name(name)
            #return sql.read_by_name(name)

    def update_contact(self):
        name, phone_exist = self.check_contact()
        if phone_exist is True:
            phone = self.input_phone()
            sql.update_db(phone, name)
            print("Contact", name, "has been updated with phone:", phone)

    def delete_contact(self):
        name, phone_exist = self.check_contact()
        if phone_exist is True:
            #contacts.pop(name)
            sql.delete_from_db(name)
            print("Contact with name ", name, " has been removed")

    def display_results(self):
        print(self.read_contact())


class Controller(SQL,Operations):
    def __init__(self, connection_type):
        self.connection_type = connection_type
    #
    # def read_config(self):
    #     config = configparser.ConfigParser()
    #     config.read('config.ini')
    #     file_type = config['DEFAULT']['file_type']
    #     return file_type


    def read_by_name(self, name):
        self.connection_type.read_by_name(name)


    # def save_into_file(self, name):
    #     self.file_type.save_into_file(name)


    def choose_operation(self):
        execute = False
        #self.read_from_file()
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
    sql = SQL()
    controller = Controller(connection_type=SQL())
    controller.choose_operation()
