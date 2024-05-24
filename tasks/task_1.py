from typing import Optional


class ObjList:
    def __init__(self, data):
        self.__data: str = data
        self.__next: Optional[ObjList] = None
        self.__prev: Optional[ObjList] = None

    @property
    def next(self) -> Optional['ObjList']:
        return self.__next

    @next.setter
    def next(self, obj):
        self.__next = obj

    @property
    def prev(self) -> Optional['ObjList']:
        return self.__prev

    @prev.setter
    def prev(self, obj):
        self.__prev = obj

    @property
    def data(self) -> str:
        return self.__data

    @data.setter
    def data(self, obj_data: str):
        self.__data = obj_data


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_obj(self, obj):
        if self.head is None:
            self.head = obj
        elif self.tail is None:
            self.tail = obj
            self.head.next = self.tail
            self.tail.prev = self.head
        else:
            self.tail.next = obj
            self.tail.next.prev = self.tail
            self.tail = self.tail.next

    def remove_obj(self) -> str | None:
        if not self.head:
            return 'Список пуст!'
        elif self.head.next is None:
            self.head = None
        else:
            pre_last = self.tail.prev
            pre_last.next = None
            self.tail.prev = None

    def get_data(self) -> list:
        list_data: list = []
        current_obj = self.head
        while current_obj is not None:
            list_data.append(current_obj.data)
            current_obj = current_obj.next
        return list_data
