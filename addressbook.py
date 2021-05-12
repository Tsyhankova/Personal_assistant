from collections import UserDict
from datetime import datetime, timedelta
from helpers import BOT_HANDLERS, INTENTS, ACTIONS, TAGS
from prettytable import PrettyTable
import pickle
import random
import re


class NameError1(Exception):
    pass


class NameError2(Exception):
    pass


class NameError3(Exception):
    pass


class NameError4(Exception):
    pass


class NameError5(Exception):
    pass


class NameError6(Exception):
    pass


class NameError7(Exception):
    pass

class NameError8(Exception):
    pass

class Adressbook(UserDict):
    def add_Record(self, name, value, type_value="phone"):
        if self.data == dict():
            myRecord = {name: {type_value: value}}
        else:
            myRecord = self.data
        return myRecord

    def change_Record(self, name, value):
        self.data.update({name: value})
        return self.data

class Field(Adressbook):
    def __init__(self):
        self.__value = ""

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Name(Field):
    def is_name(self, field):
        for key in self.data.keys():
            if key == field:
                return True


class Phone(Field):
    def is_phone(self, field):
        for value_list in self.data.values():
            for v in value_list["phone"]:
                if v == field:
                    return True


class Birthday(Field):
    def is_birthday(self, field):
        for v in self.data.values():
            if v["birthday"] == field:
                return True


class Email(Field):
    def is_email(self, field):
        for value_list in self.data.values():
            for v in value_list["email"]:
                if v == field:
                    return True


class Address(Field):
    def is_address(self, field):
        for v in self.data.values():
            if v["address"] == field:
                return True

class Notes(Field):
    def is_note(self, field):
        for value_list in self.data.values():
            for v in value_list["notes"]:
                if v == field:
                    return True


class Record(Name, Phone, Birthday, Email, Address, Notes):
    def __init__(self):
        self.name = ""
        self.phone = []
        self.birthday = ""
        self.email = []
        self.address = ""
        self.notes = []
        self.data = {}

    def __add_item_phone(self, name, phone):
        if "phone" in self.data[name]:
            self.data[name]["phone"].append(phone)
        else:
            self.data[name]["phone"] = [phone]

    def __add_item_email(self, name, email):
        if "email" in self.data[name]:
            self.data[name]["email"].append(email)
        else:
            self.data[name]["email"] = [email]

    def __add_item_notes(self, name, note):
        if "notes" in self.data[name]:
            self.data[name]["notes"].append(note)
        else:
            self.data[name]["notes"] = [note]

    def __add_phone(self, name, phone):
        if not self.is_name(name):
            self.data = self.add_Record(name, {"phone": [phone]})
            self.data = self.change_Record(name, {"phone": [phone]})
        else:
            self.__add_item_phone(name, phone)
            self.data = self.change_Record(name, self.data.get(name))
        answer = random.choice(BOT_HANDLERS["actions"]["addcontact"]["responses"])
        temp = f"I have added phone-number {phone} to {name.capitalize()}"
        return answer + ": " + temp

    def __add_birthday(self, name, birthday):
        if not self.is_name(name):
            self.data = self.add_Record(name, {"birthday": birthday}, "birthday")
            self.data = self.change_Record(name, {"birthday": birthday})
        else:
            self.data[name]["birthday"] = birthday
            self.data = self.change_Record(name, self.data.get(name))
        answer = random.choice(BOT_HANDLERS["actions"]["addcontact"]["responses"])
        temp1 = f"I have added date of birthday {birthday} to {name.capitalize()}"
        temp2 = str(self.day_to_birthday(name)) + " days to birthday"
        return answer + ": " + temp1 + " - " + temp2

    def __add_email(self, name, email):
        if not self.is_name(name):
            self.data = self.add_Record(name, {"email": [email]}, "email")
            self.data = self.change_Record(name, {"email": [email]})
        else:
            self.__add_item_email(name, email)
            self.data = self.change_Record(name, self.data.get(name))
        answer = random.choice(BOT_HANDLERS["actions"]["addcontact"]["responses"])
        temp = f"I have added email {email} to {name.capitalize()}"
        return answer + ": " + temp

    def __add_address(self, name, address):
        if not self.is_name(name):
            self.data = self.add_Record(name, {"address": address.capitalize()}, "address")
            self.data = self.change_Record(name, {"address": address.capitalize()})
        else:
            self.data[name]["address"] = address.capitalize()
            self.data = self.change_Record(name, self.data.get(name))
        answer = random.choice(BOT_HANDLERS["actions"]["addcontact"]["responses"])
        temp = f"I have added address: {address} to {name.capitalize()}"
        return answer + ": " + temp

    def __add_notes(self, name, note):
        if not self.is_name(name):
            self.data = self.add_Record(name, {"notes": [note]}, "notes")
            self.data = self.change_Record(name, {"notes": [note]})
        else:
            self.__add_item_notes(name, note)
            self.data = self.change_Record(name, self.data.get(name))
        answer = random.choice(BOT_HANDLERS["actions"]["addnotes"]["responses"])
        temp = f"I have added note to {name}"
        return answer + ": " + temp

    def __change_phone(self, name, old_phone, new_phone):
        if self.is_name(name):
            if self.is_phone(old_phone):
                self.data[name]["phone"].remove(old_phone)
                self.__add_item_phone(name, new_phone)
                self.data = self.change_Record(name, self.data.get(name))
                answer = random.choice(BOT_HANDLERS["actions"]["changecontact"]["responses"])
                temp = f"I have changed phone-number {name.capitalize()}, was:{old_phone} the new one:{new_phone}"
                return answer + ": " + temp
            else:
                raise NameError4
        else:
            raise NameError3

    def __change_birthday(self, name, old_birthday, new_birthday):
        if self.is_name(name):
            if self.is_birthday(old_birthday):
                self.data[name]["birthday"] = new_birthday
                self.data = self.change_Record(name, self.data.get(name))
                answer = random.choice(BOT_HANDLERS["actions"]["changecontact"]["responses"])
                temp1 = f"I have changed date of birthday {name.capitalize()}"
                temp2 = str(self.day_to_birthday(name)) + " days to birthday"
                return answer + ": " + temp1 + " - " + temp2
            else:
                raise NameError5
        else:
            raise NameError3

    def __change_email(self, name, old_email, new_email):
        if self.is_name(name):
            if self.is_email(old_email):
                self.data[name]["email"].remove(old_email)
                self.__add_item_email(name, new_email)
                self.data = self.change_Record(name, self.data.get(name))
                answer = random.choice(BOT_HANDLERS["actions"]["changecontact"]["responses"])
                temp = f"I hane changed email {name.capitalize()}"
                return answer + ": " + temp
            else:
                raise NameError6
        else:
            raise NameError3

    def __change_address(self, name, old_address, new_address):
        if self.is_name(name):
            if self.is_address(old_address):
                self.data[name]["address"] = new_address
                self.data = self.change_Record(name, self.data.get(name))
                answer = random.choice(BOT_HANDLERS["actions"]["changecontact"]["responses"])
                temp = f"I have changed address {name.capitalize()}"
                return answer + ": " + temp
            else:
                raise NameError7
        else:
            raise NameError3

    def __change_notes(self, name, old_note, new_note):
        if self.is_name(name):
            if self.is_note(old_note):
                self.data[name]["notes"].remove(old_note)
                self.__add_item_notes(name, new_note)
                self.data = self.change_Record(name, self.data.get(name))
                answer = random.choice(BOT_HANDLERS["actions"]["changenotes"]["responses"])
                temp = f"I have changed note to {name.capitalize()}"
                return answer + ": " + temp
            else:
                raise NameError1
        else:
            raise NameError3

    def __delete_phone(self, name, phone):
        if self.is_name(name):
            if self.is_phone(phone):
                self.data[name]["phone"].remove(phone)
                if self.data[name]["phone"] == []:
                    self.data[name].pop("phone")
                self.data = self.change_Record(name, self.data.get(name))
                answer = random.choice(BOT_HANDLERS["actions"]["deletecontact"]["responses"])
                temp = f"I have deleted phone-number {phone}"
                if self.data[name] == {}:
                    self.data.pop(name)
                return answer + ": " + temp
            else:
                raise NameError4
        else:
            raise NameError3

    def __delete_birthday(self, name, birthday):
        if self.is_name(name):
            if self.is_birthday(birthday):
                self.data[name].pop("birthday")
                self.data = self.change_Record(name, self.data.get(name))
                answer = random.choice(BOT_HANDLERS["actions"]["deletecontact"]["responses"])
                temp = f"I have deleted date of birthday {name.capitalize()}"
                if self.data[name] == {}:
                    self.data.pop(name)
                return answer + ": " + temp
            else:
                raise NameError5
        else:
            raise NameError3

    def __delete_email(self, name, email):
        if self.is_name(name):
            if self.is_email(email):
                self.data[name]["email"].remove(email)
                if self.data[name]["email"] == []:
                    self.data[name].pop("email")
                self.data = self.change_Record(name, self.data.get(name))
                answer = random.choice(BOT_HANDLERS["actions"]["deletecontact"]["responses"])
                temp = f"I have deleted email {email}"
                if self.data[name] == {}:
                    self.data.pop(name)
                return answer + ": " + temp
            else:
                raise NameError6
        else:
            raise NameError3

    def __delete_address(self, name, address):
        if self.is_name(name):
            if self.is_address(address):
                self.data[name].pop("address")
                self.data = self.change_Record(name, self.data.get(name))
                answer = random.choice(BOT_HANDLERS["actions"]["deletecontact"]["responses"])
                temp = f"I have deleted address {address}"
                if self.data[name] == {}:
                    self.data.pop(name)
                return answer + ": " + temp
            else:
                raise NameError7
        else:
            raise NameError3

    def __delete_notes(self, name, note):
        if self.is_name(name):
            if self.is_note(note):
                self.data[name]["notes"].remove(note)
                if self.data[name]["notes"] == []:
                    self.data[name].pop("notes")
                self.data = self.change_Record(name, self.data.get(name))
                answer = random.choice(BOT_HANDLERS["actions"]["deletenotes"]["responses"])
                temp = f"I have deleted note {note}"
                if self.data[name] == {}:
                    self.data.pop(name)
                return answer + ": " + temp
            else:
                raise NameError1
        else:
            raise NameError3

    def addcontact(self, name, value):
        self.value = value
        if re.match(r"\d{3}-\d{3}-\d{2}-\d{2}", self.value):
            return self.__add_phone(name, self.value)
        elif re.match(r"\d{2}-\d{2}-\d{4}", self.value):
            _ = datetime.strptime(self.value, "%d-%m-%Y")
            return self.__add_birthday(name, self.value)
        elif re.match(r"(\w|\.|\_|\-)+[@](\w|\.|\_|\-)+[.]\w{2,3}", self.value):
            return self.__add_email(name, self.value)
        elif re.match(r"\w+", self.value):
            return self.__add_address(name, self.value)
        else:
            raise ValueError

    def addnotes(self, name, tag, value):
        if tag in TAGS:
            self.value = "{}:{}".format(tag, value)
            return self.__add_notes(name, self.value)
        else:
            raise NameError2

    def changecontact(self, name, old_value, new_value):
        self.value = new_value
        if re.match(r"\d{3}-\d{3}-\d{2}-\d{2}", self.value):
            return self.__change_phone(name, old_value, self.value)
        elif re.match(r"\d{2}-\d{2}-\d{4}", self.value):
            return self.__change_birthday(name, old_value, self.value)
        elif re.match(r"(\w|\.|\_|\-)+[@](\w|\.|\_|\-)+[.]\w{2,3}", self.value):
            return self.__change_email(name, old_value, self.value)
        elif re.match(r"\w+", self.value):
            return self.__change_address(name, old_value, self.value)
        else:
            raise ValueError

    def changenotes(self, name, tag, old_value, new_value):
        if tag in TAGS:
            temp_value = "{}:{}".format(tag, old_value)
            self.value = "{}:{}".format(tag, new_value)
            return self.__change_notes(name, temp_value, self.value)
        else:
            raise NameError2

    def deletecontact(self, name, value):
        self.value = value
        if re.match(r"\d{3}-\d{3}-\d{2}-\d{2}", self.value):
            return self.__delete_phone(name, self.value)
        elif re.match(r"\d{2}-\d{2}-\d{4}", self.value):
            return self.__delete_birthday(name, self.value)
        elif re.match(r"(\w|\.|\_|\-)+[@](\w|\.|\_|\-)+[.]\w{2,3}", self.value):
            return self.__delete_email(name, self.value)
        elif re.match(r"\w+", self.value):
            return self.__delete_address(name, self.value)
        else:
            raise ValueError

    def deletenotes(self, name, tag, value):
        if tag in TAGS:
            self.value = "{}:{}".format(tag, value)
            return self.__delete_notes(name, self.value)
        else:
            raise NameError2

    def findcontact(self, arg, name):
        if self.is_name(name):
            answer = random.choice(BOT_HANDLERS["actions"]["findcontact"]["responses"])
            temp = str(self.day_to_birthday(name)) + " days to birthday"
            args = ('phone', 'birthday', 'email', 'address', 'notes')
            if arg == "all":
                return f" {answer}:\n Just reminder, {name.capitalize()} has {temp}\n" + self.datatable({name:self.data.get(name)})
            elif [i for i in args if i == arg] == [arg]:
                tab = PrettyTable(["name", arg])
                if type(self.data.get(name).get(arg)) == list:
                    _arg = ''
                    for a in self.data.get(name).get(arg):
                        _arg += f"{a}\n"
                    tab.add_row([name.capitalize(), _arg])
                else:
                    tab.add_row([name.capitalize(), self.data.get(name).get(arg)])
                return answer + "\n" + tab.get_string(title=f"{name.capitalize()} has {temp}")
            else:
                raise KeyError
        else:
            raise NameError3

    def hello(self):
        return random.choice(BOT_HANDLERS["intents"]["hello"]["responses"])

    def datatable(self, data):
        tabl_head = ['name', 'phone', 'birthday', 'email', 'address', 'notes']
        table = PrettyTable(tabl_head)
        for name, values in data.items():
            tabl = ['', '', '', '', '', '']
            tabl[0] = name.capitalize()
            for key, value in values.items():
                if key == "phone":
                    _phone = ''
                    for phone in value:
                        _phone += f"{phone}\n"
                    tabl[1] = _phone
                elif key == "birthday":
                    tabl[2] = value
                elif key == "email":
                    _email = ''
                    for email in value:
                        _email += f"{email}\n"
                    tabl[3] = _email
                elif key == "address":
                    tabl[4] = value
                elif key == "notes":
                    _note = ''
                    for note in value:
                        _note += f"{note}\n"
                    tabl[5] = _note
            table.add_row(tabl)
            tabl.clear()
        return table.get_string(title="Client's database")

    def showall(self):
        answer = random.choice(BOT_HANDLERS["intents"]["show"]["responses"])
        return answer + "\n" + self.datatable(self.data)

    def search(self, contact):
        if contact[0] == "#":
            contact = contact[1:]
        Search_result = {}
        for key, value in self.data.items():
            act_1 = re.search(str(contact.lower()), str(value).lower())
            act_2 = re.search(str(contact.lower()), str(key).lower())
            if act_1 or act_2:
                Search_result[key.capitalize()] = value
        if Search_result == {}:
            return "Nothig has found"
        answer = random.choice(BOT_HANDLERS["actions"]["search"]["responses"])
        return answer + "\n" + self.datatable(Search_result)

    def ausgang(self):
        return random.choice(BOT_HANDLERS["intents"]["exit"]["responses"])

    def day_to_birthday(self, name):
        my_date_str = self.data[name]["birthday"]
        my_date = datetime.strptime(my_date_str, "%d-%m-%Y")
        date_birthday = timedelta(days=my_date.timetuple().tm_yday)
        date_now = timedelta(days=datetime.now().timetuple().tm_yday)
        oldyear = timedelta(days=datetime(year=1, month=12, day=31).timetuple().tm_yday)
        newyear = timedelta(days=datetime(year=1, month=1, day=1).timetuple().tm_yday)
        if date_birthday == date_now:
            result = 0
        elif date_birthday > date_now:
            result = date_birthday - date_now
        else:
            result = (oldyear - date_now) + (date_birthday - newyear)
        return result.days

    def help(self, commands, arguments):
        result = "\n\tYou can write next commands for working with me:\n"
        for command in commands.keys():
            result += "\n\t" + str(command) + " " + str(arguments[command])
        answer = random.choice(BOT_HANDLERS["intents"]["help"]["responses"])
        return answer + " " + result

    def givepeoplebirthday(self, number):
        result = ""
        bd = {}
        for name in self.data.keys():
            if self.day_to_birthday(name) in range(int(number)):
                temp = str(self.day_to_birthday(name)) + " days to birthday"
                bd[name.capitalize()] = self.data[name]
                result += f"\n{str(name.capitalize())} - {str(temp)}"
        if result:
            answer = random.choice(BOT_HANDLERS["actions"]["nearbirthday"]["responses"])
            return f"{answer}\n {result}\n {self.datatable(bd)}"
        else:
            return f"Nobody has birthday in {number} days"

    def findname(self, part_name):
        result = ""
        for name in self.data.keys():
            if re.findall(part_name, name):
                temp = str(self.day_to_birthday(name)) + " days to birthday"
                result += "\n\t\t\t" + str(name.capitalize()) + " " + str(self.data[name]) + " - " + str(temp)
        if result:
            answer = random.choice(BOT_HANDLERS["actions"]["name"]["responses"])
            return answer + " " + result
        else:
            raise NameError3

    def findphone(self, part_phone):
        result = ""
        for name in self.data.keys():
            if "phone" in self.data[name]:
                for elem in self.data[name]["phone"]:
                    if re.findall(part_phone, elem):
                        temp = str(self.day_to_birthday(name)) + " days to birthday"
                        result += "\n\t\t\t" + str(name.capitalize()) + " " + str(elem) + " - " + str(temp)
        if result:
            answer = random.choice(BOT_HANDLERS["actions"]["phone"]["responses"])
            return answer + " " + result
        else:
            raise NameError4

    def findbirthday(self, part_birthday):
        result = ""
        for name in self.data.keys():
            if "birthday" in self.data[name]:
                temp = self.data[name]["birthday"]
                if re.findall(part_birthday, temp):
                    temp_str = str(self.day_to_birthday(name)) + " days to birthday"
                    result += "\n\t\t\t" + str(name.capitalize()) + " " + str(temp) + " - " + str(temp_str)
        if result:
            answer = random.choice(BOT_HANDLERS["actions"]["birthday"]["responses"])
            return answer + " " + result
        else:
            raise NameError5

    def findemail(self, part_email):
        result = ""
        for name in self.data.keys():
            if "email" in self.data[name]:
                for elem in self.data[name]["email"]:
                    if re.findall(part_email, elem):
                        temp = str(self.day_to_birthday(name)) + " days to birthday"
                        result += "\n\t\t\t" + str(name.capitalize()) + " " + str(elem) + " - " + str(temp)
        if result:
            answer = random.choice(BOT_HANDLERS["actions"]["email"]["responses"])
            return answer + " " + result
        else:
            raise NameError6

    def findaddress(self, part_address):
        result = ""
        for name in self.data.keys():
            if "address" in self.data[name]:
                temp = self.data[name]["address"]
                if re.findall(part_address, temp):
                    temp_str = str(self.day_to_birthday(name)) + " days to birthday"
                    result += "\n\t\t\t" + str(name.capitalize()) + " " + str(temp) + " - " + str(temp_str)
        if result:
            answer = random.choice(BOT_HANDLERS["actions"]["address"]["responses"])
            return answer + " " + result
        else:
            raise NameError7

    def findbytag(self, tag):
        result = ""
        for name in self.data.keys():
            if "notes" in self.data[name]:
                for elem in self.data[name]["notes"]:
                    if re.findall(tag, elem):
                        temp = str(self.day_to_birthday(name)) + " days to birthday"
                        result += "\n\t\t\t" + str(name.capitalize()) + " " + str(elem) + " - " + str(temp)
        if result:
            answer = random.choice(BOT_HANDLERS["actions"]["findbytag"]["responses"])
            return answer + " " + result
        else:
            raise NameError1

