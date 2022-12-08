from datetime import date

from view import Index, Contacts


# front-controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


def navigation_front(request):
    urls = {item.__class__.__name__.lower(): key for key, item in routers.items()}
    request['urls'] = urls


fronts = [secret_front, other_front, navigation_front]

routers = {
    '/': Index(),
    '/contacts/': Contacts()
}
