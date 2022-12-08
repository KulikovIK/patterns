from simple_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html',
                                date=request.get('date', None),
                                navigation=request.get('navigation', None),
                                name=self.__class__.__name__.lower())


class Contacts:
    def __call__(self, request):
        return '200 OK', render('contact.html',
                                date=request.get('date', None),
                                urls=request.get('urls', None),
                                name=self.__class__.__name__.lower())
