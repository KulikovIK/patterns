from simple_framework.contenttype_handler import get_content
from simple_framework.main import Framework, PageNotFound404
from simple_framework.request_handlers import PostRequests, GetRequests



class ConsoleLogger(Framework):
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

		print(f'Поступил {method} запрос с параметрами: {request.get("request_params")}')

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