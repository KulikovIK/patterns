from wsgiref.simple_server import make_server

from simple_framework.main import Framework
from urls import routers, fronts

application = Framework(routers, fronts)

with make_server('', 8080, application) as httpd:
    print("Запуск сервера на порту 8080")
    httpd.serve_forever()
