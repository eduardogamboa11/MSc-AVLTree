import timeit
import unicodedata

class Contact:
    def __init__(self, name, last_name, phone_number, address, email, networks):
        self.name = name
        self.last_name = last_name
        self.phone_number = int(phone_number)
        self.address = address
        self.email = email
        self.networks = networks
        self.left = None
        self.right = None

    def __str__(self):
        return "name: {} {}, phone:{}, address:{}, email:{}," \
               " network(s):{}".format(self.name, self.last_name, self.phone_number, self.address,
                                       self.email, self.networks)


class AVLTree:
    def __init__(self):
        self.node = None
        self.height = -1
        self.balance = 0

    def insert(self, key):
        n = Contact(key.name, key.last_name, key.phone_number, key.address, key.email, key.networks)
        if self.node is None:
            self.node = n
            self.node.left = AVLTree()
            self.node.right = AVLTree()
        elif key.phone_number < self.node.phone_number:
            self.node.left.insert(key)
        elif key.phone_number > self.node.phone_number:
            self.node.right.insert(key)
        self.rebalance()

    def insert_name(self, key):
        n = Contact(key.name, key.last_name, key.phone_number, key.address, key.email, key.networks)
        if self.node is None:
            self.node = n
            self.node.left = AVLTree()
            self.node.right = AVLTree()
        elif key.name < self.node.name:
            self.node.left.insert_name(key)
        elif key.name > self.node.name:
            self.node.right.insert_name(key)
        self.rebalance()

    def insert_last_name(self, key):
        n = Contact(key.name, key.last_name, key.phone_number, key.address, key.email, key.networks)
        if self.node is None:
            self.node = n
            self.node.left = AVLTree()
            self.node.right = AVLTree()
        elif key.last_name < self.node.last_name:
            self.node.left.insert_last_name(key)
        elif key.last_name > self.node.last_name:
            self.node.right.insert_last_name(key)
        self.rebalance()

    def rebalance(self):
        self.update_heights(recursive=False)
        self.update_balances(False)
        while self.balance < -1 or self.balance > 1:
            if self.balance > 1:
                if self.node.left.balance < 0:
                    self.node.left.rotate_left()
                    self.update_heights()
                    self.update_balances()
                self.rotate_right()
                self.update_heights()
                self.update_balances()
            if self.balance < -1:
                if self.node.right.balance > 0:
                    self.node.right.rotate_right()
                    self.update_heights()
                    self.update_balances()
                self.rotate_left()
                self.update_heights()
                self.update_balances()

    def update_heights(self, recursive=True):
        if self.node:
            if recursive:
                if self.node.left:
                    self.node.left.update_heights()
                if self.node.right:
                    self.node.right.update_heights()

            self.height = 1 + max(self.node.left.height, self.node.right.height)
        else:
            self.height = -1

    def update_balances(self, recursive=True):
        if self.node:
            if recursive:
                if self.node.left:
                    self.node.left.update_balances()
                if self.node.right:
                    self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height
        else:
            self.balance = 0

    def rotate_right(self):
        new_root = self.node.left.node
        new_left_sub = new_root.right.node
        old_root = self.node

        self.node = new_root
        old_root.left.node = new_left_sub
        new_root.right.node = old_root

    def rotate_left(self):
        new_root = self.node.right.node
        new_left_sub = new_root.left.node
        old_root = self.node

        self.node = new_root
        old_root.right.node = new_left_sub
        new_root.left.node = old_root

    def delete(self, key):
        if self.node is not None:
            if self.node.phone_number == key:
                if not self.node.left.node and not self.node.right.node:
                    self.node = None
                elif not self.node.left.node:
                    self.node = self.node.right.node
                elif not self.node.right.node:
                    self.node = self.node.left.node
                else:
                    successor = self.node.right.node
                    while successor and successor.left.node:
                        successor = successor.left.node
                    if successor:
                        self.node.phone_number = successor.phone_number
                        self.node.right.delete(successor.phone_number)
            elif key < self.node.phone_number:
                self.node.left.delete(key)

            elif key > self.node.phone_number:
                self.node.right.delete(key)
            self.rebalance()

    def delete_name(self, key):
        if self.node is not None:
            if self.node.name == key:
                if not self.node.left.node and not self.node.right.node:
                    self.node = None
                elif not self.node.left.node:
                    self.node = self.node.right.node
                elif not self.node.right.node:
                    self.node = self.node.left.node
                else:
                    successor = self.node.right.node
                    while successor and successor.left.node:
                        successor = successor.left.node
                    if successor:
                        self.node.name = successor.name
                        self.node.right.delete_name(successor.name)
            elif key < self.node.name:
                self.node.left.delete_name(key)

            elif key > self.node.name:
                self.node.right.delete_name(key)
            self.rebalance()

    def delete_last_name(self, key):
        if self.node is not None:
            if self.node.last_name == key:
                if not self.node.left.node and not self.node.right.node:
                    self.node = None
                elif not self.node.left.node:
                    self.node = self.node.right.node
                elif not self.node.right.node:
                    self.node = self.node.left.node
                else:
                    successor = self.node.right.node
                    while successor and successor.left.node:
                        successor = successor.left.node
                    if successor:
                        self.node.last_name = successor.last_name
                        self.node.right.delete_last_name(successor.last_name)
            elif key < self.node.last_name:
                self.node.left.delete_last_name(key)

            elif key > self.node.last_name:
                self.node.right.delete_last_name(key)
            self.rebalance()

    def search_tree(self, key):
        value = self.node
        while True:
            if key < value.phone_number:
                if value.left.node is None:
                    break
                else:
                    value = value.left.node
            elif key > value.phone_number:
                if value.right.node is None:
                    break
                else:
                    value = value.right.node
            else:
                return value

    def search_name_tree(self, key):
        value = self.node
        if value is None:
            return
        while True:
            if key < value.name:
                if value.left.node is None:
                    break
                else:
                    value = value.left.node
            elif key > value.name:
                if value.right.node is None:
                    break
                else:
                    value = value.right.node
            else:
                return value

    def search_last_name_tree(self, key):
        value = self.node
        if value is None:
            return
        while True:
            if key < value.last_name:
                if value.left.node is None:
                    break
                else:
                    value = value.left.node
            elif key > value.last_name:
                if value.right.node is None:
                    break
                else:
                    value = value.right.node
            else:
                return value


class HashTable:
    def __init__(self):
        self.size = 4
        self.data = [None] * self.size

    def get_number_hash(self, value):
        return int(1000000000/value) % self.size

    def get_alpha_hash(self, value):
        total_value = 0
        for i in range(len(value)):
            total_value += ord(value[i])
        return int(1000000000/total_value) % self.size

    def insert_value(self, value):
        hash_value = self.get_number_hash(value.phone_number)
        if self.data[hash_value] is None:
            self.data[hash_value] = AVLTree()
        else:
            pass
        self.data[hash_value].insert(value)

    def insert_name_value(self, value):
        hash_value = self.get_alpha_hash(value.name)
        if self.data[hash_value] is None:
            self.data[hash_value] = AVLTree()
        else:
            pass
        self.data[hash_value].insert_name(value)

    def insert_last_name_value(self, value):
        hash_value = self.get_alpha_hash(value.last_name)
        if self.data[hash_value] is None:
            self.data[hash_value] = AVLTree()
        else:
            pass
        self.data[hash_value].insert_last_name(value)

    def search_value(self, key):
        bucket = hash_phone_table.get_number_hash(key)
        if self.data[bucket] is None:
            pass
        else:
            search_result = self.data[bucket].search_tree(key)
            if search_result is None:
                pass
            else:
                return search_result

    def search_name_value(self, key):
        bucket = hash_name_table.get_alpha_hash(key)
        if self.data[bucket] is None:
            pass
        else:
            search_result = self.data[bucket].search_name_tree(key)
            if search_result is None:
                pass
            else:
                return search_result

    def search_last_name_value(self, key):
        bucket = hash_last_name_table.get_alpha_hash(key)
        if self.data[bucket] is None:
            pass
        else:
            search_result = self.data[bucket].search_last_name_tree(key)
            if search_result is None:
                pass
            else:
                return search_result

###DELETE###
    def delete_hash(self, key):
        hash_position = self.get_number_hash(key)
        if hash_phone_table.data[hash_position] is None:
            print("Contact not found")
        else:
            contact = hash_phone_table.data[hash_position].search_tree(key)
            if contact is None:
                pass
            else:
                print(contact)
                hash_phone_table.data[hash_position].delete(contact.phone_number)
                print("Contact deleted")

    def delete_name_hash(self, key):
        hash_position = self.get_alpha_hash(key)
        if hash_name_table.data[hash_position] is None:
            print("Contact not found")
        else:
            contact = hash_name_table.data[hash_position].search_name_tree(key)
            if contact is None:
                pass
            else:
                hash_name_table.data[hash_position].delete_name(contact.name)

    def delete_last_name_hash(self, key):
        hash_position = self.get_alpha_hash(key)
        if hash_last_name_table.data[hash_position] is None:
            print("Contact not found")
        else:
            contact = hash_last_name_table.data[hash_position].search_last_name_tree(key)
            if contact is None:
                pass
            else:
                hash_last_name_table.data[hash_position].delete_last_name(contact.last_name)

###EDIT###
    def edit_hash(self, key):
        hash_position = self.get_number_hash(key)
        if self.data[hash_position] is None:
            print("Contact not found")
        else:
            contact = self.data[hash_position].search_tree(key)
            new_contact = contact
            self.data[hash_position].delete(contact.phone_number)
            if new_contact is None:
                pass
            else:
                while True:
                    field = str(input("Please enter field to edit:\nOptions are phone, address, email and network\n"
                                      "to stop editing and save contact press 1\n "))
                    if field == 'name' or field == 'last name':
                        print("This field can't be modified")
                    elif field == 'phone':
                        new_info = int(input("Please enter new phone number: "))
                        new_contact.phone_number = new_info
                    elif field == 'address':
                        new_info = str(input("Please enter new address: "))
                        new_contact.address = new_info
                    elif field == 'email':
                        new_info = str(input("Please enter new email: "))
                        new_contact.email = new_info
                    elif field == 'network' or field == 'networks':
                        new_info = str(input("Please enter new network: "))
                        new_contact.networks = new_info
                    elif field == '1':
                        new_phone_position = hash_phone_table.get_number_hash(new_contact.phone_number)
                        print("New contact info is:",new_contact)
                        self.data[new_phone_position].insert(new_contact)
                        new_name_position = hash_name_table.get_alpha_hash(new_contact.name)
                        hash_name_table.data[new_name_position].insert_name(new_contact)
                        new_last_name_position = hash_last_name_table.get_alpha_hash(new_contact.last_name)
                        hash_last_name_table.data[new_last_name_position].insert_last_name(new_contact)
                        break
                    else:
                        print("Please enter a valid option")


contact1 = Contact("eduardo", "gamboa", 3314373238, "mezquite", "eg95@gmail.com", "eduardogamboa58")
contact2 = Contact("carlos", "barraza", 1111, "address2", "mail2@gmail.com", "network2")
contact3 = Contact("mauricio", "martinez", 7, "address3", "mail3@gmail.com", "network3")
contact4 = Contact("alberto", "torres", 1114, "address4", "mail4@gmail.com", "network4")
contact5 = Contact("yolanda", "lopez", 1115, "address5", "mail5@gmail.com", "network5")
contact6 = Contact("miguel", "tapia", 1116, "address6", "mail6@gmail.com", "network6")
contact7 = Contact("luis", "hernandez", 1117, "address7", "mail7@gmail.com", "network7")
contact8 = Contact("fernando", "gomez", 1118, "address8", "mail8@gmail.com", "network8")
contact9 = Contact("erika", "ruiz", 1119, "address9", "mail9@gmail.com", "network9")
contact10 = Contact("guillermo", "perez", 1121, "address10", "mail10@gmail.com", "network10")
contact11 = Contact("ivan", "valdez", 1122, "address11", "mail11@gmail.com", "network11")
contact12 = Contact("hector", "gonzalez", 1123, "address12", "mail12@gmail.com", "network12")
contact13 = Contact("francisco", "corona", 1124, "address13", "mail13@gmail.com", "network13")
contact14 = Contact("jose", "diaz", 1125, "address14", "mail14@gmail.com", "network14")
contact15 = Contact("jorge", "garcia", 1126, "address15", "mail15@gmail.com", "network15")
contact16 = Contact("diana", "sanchez", 1127, "address16", "mail16@gmail.com", "network16")
contact17 = Contact("paola", "flores", 1128, "address17", "mail17@gmail.com", "network17")
contact18 = Contact("pedro", "medina", 1129, "address18", "mail18@gmail.com", "network18")
contact19 = Contact("gustavo", "rios", 1131, "address19", "mail19@gmail.com", "network19")
contact20 = Contact("jesus", "dominguez", 1132, "address20", "mail20@gmail.com", "network20")


hash_name_table = HashTable()
hash_phone_table = HashTable()
hash_last_name_table = HashTable()

contact_list = [contact1, contact2, contact3, contact4, contact5, contact6, contact7, contact8, contact9,
                contact10, contact11, contact12, contact13, contact14, contact15, contact16, contact17, contact18,
                contact19, contact20]

for contact in contact_list:
    hash_name_table.insert_name_value(contact)
    hash_last_name_table.insert_last_name_value(contact)
    hash_phone_table.insert_value(contact)

"""
total_time = 0
###TESTING TIME###
for contact in contact_list:
    start_search_time = timeit.default_timer()
    hash_name_table.delete_name_hash(contact.name)
    hash_last_name_table.delete_last_name_hash(contact.last_name)
    hash_phone_table.delete_hash(contact.phone_number)
    total_time += timeit.default_timer() - start_search_time
    print("search time {} seconds".format(timeit.default_timer() - start_search_time))
print("average time {}".format(total_time / 20))
"""
###Menu###
while True:
    user_choice = str(input("What do you want to do?\n1 - Add contact\n2 - Search contact\n"
                            "3 - Edit contact\n4 - Delete contact\n5 - Exit\n"))
    ###leave program###
    if user_choice == '5':
        break

    ###add contact###
    elif user_choice == '1':
        print("To add a contact please enter the next fields")
        name = str(input("Name(s): "))
        last_name = str(input("Last name(s): "))
        phone_number = int(input("Phone number: "))
        address = str(input("Address: "))
        email = str(input("Email: "))
        networks = str(input("Network(s): "))

        contact = Contact(name, last_name, phone_number, address, email, networks)
        contact_exist = hash_phone_table.search_value(contact.phone_number)
        if contact_exist is None:
            hash_name_table.insert_name_value(contact)
            hash_last_name_table.insert_last_name_value(contact)
            hash_phone_table.insert_value(contact)
            print("Contact added:",contact)
        else:
            print("This number already exist")
            print(contact_exist)

    ###search contact###
    elif user_choice == '2':
        field_choice = input("Please enter your search by name, last name or phone number: ")
        if field_choice.isalpha():
            name_contact = False
            contact = hash_name_table.search_name_value(field_choice)
            if contact is None:
                pass
            else:
                print(contact)
                name_contact = True
            contact = hash_last_name_table.search_last_name_value(field_choice)
            if contact is None:
                if name_contact is False:
                    print("Contact not found")
                    pass
                else:
                    pass
            else:
                print(contact)
        elif field_choice.isnumeric():
            contact = hash_phone_table.search_value(int(field_choice))
            if contact is None:
                print("Contact not found")
            else:
                print(contact)
        else:
            print("Please enter valid search")

    ###edit contact###
    elif user_choice == '3':
        contact_number = int(input("Please enter phone number to edit contact: "))

        contact_position = hash_phone_table.get_number_hash(contact_number)
        contact = hash_phone_table.data[contact_position].search_tree(contact_number)
        hash_name_table.delete_name_hash(contact.name)
        hash_last_name_table.delete_last_name_hash(contact.last_name)
        hash_phone_table.edit_hash(contact.phone_number)

    ###delete contact###
    elif user_choice == '4':
        contact_number = int(input("Please enter phone number to delete contact: "))

        contact_position = hash_phone_table.get_number_hash(contact_number)
        contact = hash_phone_table.data[contact_position].search_tree(contact_number)
        if contact is not None:
            contact_name = contact
            contact_last_name = contact
            hash_name_table.delete_name_hash(contact.name)
            hash_last_name_table.delete_last_name_hash(contact.last_name)
            hash_phone_table.delete_hash(contact.phone_number)
        else:
            print("Contact not found")
    else:
        print("Invalid choice, please enter a valid option")

