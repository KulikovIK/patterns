from datetime import date

from view import Index, Contacts


# front-controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routers = {
    '/': Index(),
    '/contacts/': Contacts()
}
