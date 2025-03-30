from collections import UserDict
import re
from typing import Optional

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value): super().__init__(self.__validate_name(value))

    def __validate_name(self, value):
        if len(value) == 0: raise ValueError('Name is too short, need more than 0 symbol')
        else: return value 

class Phone(Field):
    pattern = r'[0-9]{10}'

    def __init__(self, value): 
        self.__value = value
        super().__init__(self.__value)

    @property
    def value(self): return self.__value

    @value.setter
    def value(self, value): 
        self.__value = self.__validate_number(value)

    def __validate_number(self, number):
        if re.fullmatch(self.pattern, number.strip()): return number
        else: raise ValueError('The "phone number" field must contain 10 digits')

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, number: str): self.phones.append(Phone(number))
    
    def remove_phone(self, number: str): self.phones = list(filter(lambda phone: phone.value!=number, self.phones))

    def edit_phone(self, number: str, new_value):
        for phone in self.phones:
            if phone.value == number:
                phone.value = new_value
                return True

        raise KeyError(f'Phone number: {number} not found')

    def find_phone(self, number:str) -> Optional[Phone]:
        for phone in self.phones:
            if phone.value == number: return phone
        
        raise KeyError(f'Phone number: {number} not found')

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        if isinstance(record, Record):
            if record.name.value not in self.data: self.data[record.name.value] = record
            else: raise KeyError(f"The {record.name.value} is already in contact list")
        else: raise ValueError(f"The {record} is not instance of Record")

    def find(self, name: str) -> Optional[Record]:
        if name in self.data: return self.data.get(name)
        else: raise KeyError(f'{name} is absent in contact list')

    def delete(self, name: str) -> Optional[Record]:
        if name in self.data: return self.data.pop(name)
        else: raise KeyError(f'{name} is absent in contact list')

if __name__ == '__main__':
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    book.delete("Jane")
