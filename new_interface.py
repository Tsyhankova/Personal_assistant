from abc import ABC, abstractmethod
from addressbook import Record, NameError1, NameError2, NameError3, NameError4, NameError5, NameError6, NameError7, NameError8
from helpers import BOT_HANDLERS, INTENTS, ACTIONS, TAGS
from new_project import input_error, parser, split_command
import pathlib
import pickle


class View(ABC):
    def __init__(self, new_record):
        self.record = new_record

    @abstractmethod
    def representation(self):
        pass


class ConsoleView(View):
    def representation(self):
        result = ""
        key = ""

        print("{:>20}{:<300}".format("Your assistant: ","Hello! Hope you are fine! Input <help> for get an instruction",))
        while True:
            if key == "" in self.record.data.keys():
                self.record.data.pop(key)
            command = input("{:>20}".format("User: "))
            kommande, argumente = split_command(command)
            if kommande not in BOT_HANDLERS["actions"]["clean"]["examples"]:
                argumente = argumente.lower().split(" ")
            result = parser(kommande, argumente, self.record)
            print("{:>20}".format(f"Your assistant:"), result)
            if result in BOT_HANDLERS["intents"]["exit"]["responses"]:
                break
        return self.record 


def main():
    my_record = Record()
    my_record.data = {
        "ivanov": {
            "phone": ["006-222-33-33", "073-888-78-89"],
            "birthday": "25-09-1953",
        },
        "petrov": {
            "phone": ["098-333-44-44", "063-999-45-56"],
            "birthday": "07-03-1983",
            "email": ["petrov@gmail.com"],
            "address": "Minsk, Pushkin st, 5",
            "notes": ["event: daughther bd party", "allergy: milk, nuts", "preference: ponny"],
        },
        "sidorov": {
            "phone": ["050-444-55-66"],
            "birthday": "14-12-1998",
        },
        "petrenko": {
            "phone": ["098-777-44-44", "050-444-55-66"],
            "birthday": "07-07-1983",
        },
        "sidorenko": {
            "phone": ["098-777-44-44", "050-444-55-66"],
            "birthday": "03-09-1983",
        },
    }

    if pathlib.Path("addressbook.bin").is_file():
        with open("addressbook.bin", "rb") as file:
            my_record = pickle.load(file)

    my_representation = ConsoleView(my_record)
    my_record = my_representation.representation()

    with open("addressbook.bin", "wb") as file:
        pickle.dump(my_record, file, 5)


if __name__ == "__main__":
    main()
