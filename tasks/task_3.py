import random
from typing import Optional


def get_server_address() -> str:
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))


class Data:
    def __init__(self, data, destination_ip):
        self.data: str = data
        self.destination_ip: str = destination_ip


class Server:
    def __init__(self):
        self.__ip_address: str = get_server_address()
        self.buffer: list[Data] = []
        self.router: Optional[Server] = None

    @property
    def ip(self) -> str:
        return self.__ip_address

    def send_data(self, data: Data):
        self.router.buffer.append(data)

    def get_data(self) -> str:
        info: str = f"Почта {self.ip}\n" + ''.join([f"Сообщение: {item.data}\n" for item in self.buffer])
        self.buffer.clear()
        return info


class Router:
    def __init__(self):
        self.servers: dict[str, Server] = {}
        self.buffer: list[Data] = []

    def link(self, obj):
        if obj.ip not in self.servers:
            self.servers[obj.ip] = obj
            obj.router = self

    def unlink(self, obj):
        self.servers.pop(obj.ip_address, None)

    def send_data(self):
        if self.buffer:
            for item in self.buffer:
                self.servers[item.destination_ip].buffer.append(item)
        self.buffer.clear()
