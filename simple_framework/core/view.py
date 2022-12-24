from components.models import Engine
from simple_framework.core.templator import render, render_css

site = Engine()


class View:
    template_name = None

    def __call__(self, request):
        return '200 OK', render(self.template_name,
                                date=request.get('date', None),
                                urls=request.get('urls', None),
                                name=self.__class__.__name__.lower())


class ListView:
    template_name = None

    def __call__(self, request):
        return '200 OK', render(self.template_name,
                                date=request.get('date', None),
                                urls=request.get('urls', None),
                                name=self.__class__.__name__.lower(),
                                objects_list=site.categories)


class Static:
    def __call__(self, request, filename):
        return '200 OK', render_css(filename)
