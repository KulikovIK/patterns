from components.models import Engine
from simple_framework.core.templator import render, render_css
from simple_framework.utils.decorators import Debug

site = Engine()


class View:
    template_name = None

    def get_context_data(self, context):
        result = {}
        result['date'] = context.get('date', None)
        result['urls'] = context.get('urls', None)
        return result

    def get_template(self):
        return self.template_name

    def render_template_with_context(self, context):
        template_name = self.get_template()
        return '200 OK', render(template_name,
                                name=self.__class__.__name__.lower(),
                                **context)

    @Debug(name=None)
    def __call__(self, request):
        context = self.get_context_data(request)
        return self.render_template_with_context(context)


class ListView(View):
    queryset = []
    template_name = None
    context_object_name = 'objects_list'

    def get_queryset(self):
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self, context, result: dict = None):
        super().get_context_data(context)
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context[context_object_name] = queryset
        return context


class CreateView(View):
    template_name = None

    @staticmethod
    def get_request_data(request):
        return request['request_params']

    def create_object(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_object(data)

            return self.render_template_with_context(request)
        else:
            return super().__call__(request)


class Static:
    def __call__(self, request, filename):
        return '200 OK', render_css(filename)
