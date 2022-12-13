from os.path import join

from jinja2 import Environment, FileSystemLoader, Template


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры
    :return:
    """

    # file_path = join(folder, template_name)
    # Открываем шаблон по имени
    # with open(file_path, encoding='utf-8') as template_file:
    #     # Читаем файл
    #     template = Template(template_file.read())

    # Работа с шаблонами
    env = Environment(loader=FileSystemLoader(folder))
    template = env.get_or_select_template(template_name)

    # рендеринг шаблона с параметрами
    return template.render(**kwargs)


def render_css(template_name, folder='static', **kwargs):
    file_path = join(folder, template_name)

    # Открываем шаблон по имени
    encoding = 'utf-8' if template_name.endswith('.css') else None
    read_mode = 'r' if template_name.endswith('.css') else 'rb'

    with open(file_path, encoding=encoding, mode=read_mode) as template_file:
        # Читаем файл
        template = Template(template_file.read())

    return template.render(**kwargs)
