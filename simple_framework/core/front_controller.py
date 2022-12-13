from datetime import date
from urls import routers
from simple_framework.core.view import Static


# front-controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


def navigation_front(request):
    urls = {item.__class__.__name__.lower(): key for key, item in routers.items()}
    request['urls'] = urls


fronts = [secret_front, other_front, navigation_front]

routers['/css/'] = Static()
