import abc


class SimpleLoger(metaclass=abc.ABCMeta):
    # def __call__(self, method: str, params: dict):
    #     return self.print_log(method, params)

    @abc.abstractmethod
    def print_log(self, method: str, params: dict) -> None:
        pass


class Loger1(SimpleLoger):

    def print_log(self, method: str, params: dict) -> None:
        log_string = f'Поступил {method} запрос с параметрами: {params}'
        with open(f'{__class__.__name__}.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(log_string + '\n')


class ConsoleWriter:

    def write(self, text):
        print(text)


class FileWriter:
    def __init__(self):
        self.file_name = 'log_file.txt'

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as file:
            file.write(f'{text}\n')


class Logger:
    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log ---> {text}'
        self.writer.write(text)
