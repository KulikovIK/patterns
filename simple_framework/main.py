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
        path = environ['PATH_INFO']

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        # находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routers_list:
            view = self.routers_list[path]
        else:
            view = PageNotFound404()
        request = {}

        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller

        for front_item in self.fronts_list:
            front_item(request)

        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
