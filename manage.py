from wsgiref.simple_server import make_server

from simple_framework.console_logger import ConsoleLogger
from simple_framework.main import Framework
from simple_framework.fake_server import FakeServer
from simple_framework.core.front_controller import routers, fronts

application = Framework(routers, fronts)
# application = FakeServer(routers, fronts)
# application = ConsoleLogger(routers, fronts)

with make_server('', 8080, application) as httpd:
    print("Запуск сервера на порту 8080")
    httpd.serve_forever()
