from typing import Optional


class ObjList:
    def __init__(self, data: str):
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
        """Метод для добавления объекта в конец списка"""
        if self.head is None:
            self.head = obj
            self.tail = obj
        else:
            obj.prev = self.tail
            self.tail.next = obj
            self.tail = obj

    def remove_obj(self):
        """Метод для удаления последнего элемента списка"""
        if self.head is self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None

    def get_data(self) -> list[str]:
        """Метод, возвращающий все информацию по каждому элементу списка"""
        list_data: list[str] = []
        current_obj = self.head
        while current_obj is not None:
            list_data.append(current_obj.data)
            current_obj = current_obj.next
        return list_data
