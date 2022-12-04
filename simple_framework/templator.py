from jinja2 import Template
from os.path import join


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры
    :return:
    """

    file_path = join(folder, template_name)
    # Открываем шаблон по имени
    with open(file_path, encoding='utf-8') as template_file:
        # Читаем файл
        template = Template(template_file.read())

    # рендеринг шаблона с параметрами
    return template.render(**kwargs)
