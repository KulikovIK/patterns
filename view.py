from simple_framework.templator import render


class BaseView:
    template_name = None

    def __call__(self, request):
        return '200 OK', render(self.template_name,
                                date=request.get('date', None),
                                urls=request.get('urls', None),
                                name=self.__class__.__name__.lower())


class Index(BaseView):
    template_name = 'index.html'


class Example(BaseView):
    template_name = 'examples.html'


class Page(BaseView):
    template_name = 'page.html'


class AnotherPage(BaseView):
    template_name = 'another_page.html'


class Contacts:
    template_name = 'contact.html'
