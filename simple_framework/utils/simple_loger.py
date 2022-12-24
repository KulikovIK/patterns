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
