from quopri import decodestring

from simple_framework.contenttype_handler import get_content
from simple_framework.request_handlers import GetRequests, PostRequests
from simple_framework.utils.simple_loger import Loger1


class PageNotFound404:
    def __call__(self, request) -> [str, str]:
        return '404 WHAT', '404 Page not found'


class Framework:
    """Класс Framework - основа фреймворка"""

    def __init__(self, routers_obj, fronts_obj):
        self.routers_list = routers_obj
        self.fronts_list = fronts_obj

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        path = environ.get('PATH_INFO')

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        # получение параметров запроса
        method = environ.get('REQUEST_METHOD')
        request['method'] = method

        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = Framework.decode_value(request_params)

        if method == 'POST':
            request_params = PostRequests().get_request_params(environ)
            request['request_params'] = Framework.decode_value(request_params)

        loger = Loger1()
        loger.print_log(method, request.get("request_params"))

        # находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routers_list:
            view = self.routers_list[path]
        elif path.endswith('.css/'):
            view = self.routers_list['/css/']
        else:
            view = PageNotFound404()

        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller

        for front_item in self.fronts_list:
            front_item(request)

        return get_content(start_response, request, path, view)

    @staticmethod
    def decode_value(data: dict) -> dict:
        decoded_data = {}
        for key, value in data.items():
            value = bytes(value.replace('%', '=').replace('+', ' '), 'utf-8')
            value = decodestring(value).decode('utf-8')
            decoded_data[key] = value

        return decoded_data
