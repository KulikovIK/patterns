from simple_framework.core.view import View


class Index(View):
    template_name = 'index.html'


class Example(View):
    template_name = 'examples.html'


class Page(View):
    template_name = 'page.html'


class AnotherPage(View):
    template_name = 'another_page.html'


class Contacts(View):
    template_name = 'contact.html'
