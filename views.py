from components.behavioral_patterns import EmailNotifier, SmsNotifier, BaseSerializer
from components.models import MapperRegistry
from simple_framework.core.view import View, ListView, CreateView, site, render
from simple_framework.utils.decorators import AppRoute, Debug
from simple_framework.utils.simple_loger import Logger
# from components.arcitect_patterns import UnitOfWork

routers = {}
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
# UnitOfWork.new_thread()
# UnitOfWork.get_thread().set_mapper_register(MapperRegistry)


@AppRoute(routers=routers, url='/')
class Index(ListView):
    queryset = site.categories
    template_name = 'index.html'

    def __call__(self, *args, **kwargs):
        logger.log('Главная')
        return super().__call__(*args)


@AppRoute(routers=routers, url='/category-list/')
class CategoryList(ListView):
    queryset = site.categories
    template_name = 'category_list.html'

    def __call__(self, *args, **kwargs):
        logger.log('Список категорй')
        return super().__call__(*args)


@AppRoute(routers=routers, url='/about/')
class About(View):
    template_name = 'about.html'


@AppRoute(routers=routers, url='/study_programs/')
class StudyPrograms(View):
    template_name = 'study-programs.html'


@AppRoute(routers=routers, url='/courses-list/')
class CoursesList:
    @Debug(name='Courses-list')
    def __call__(self, request):

        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))

            return '200 OK', render('course_list.html',
                                    urls=request.get('urls', None),
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id,
                                    )
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoute(routers=routers, url='/create-course/')
class CreateCourse:
    category_id = -1

    @Debug(name='Create-course')
    def __call__(self, request):
        if request['method'] == 'POST':

            data = request['request_params']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)

                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)

                site.courses.append(course)

            return '200 OK', render('course_list.html',
                                    urls=request.get('urls', None),
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html',
                                        urls=request.get('urls', None),
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@AppRoute(routers=routers, url='/create-category/')
class CreateCategory:
    @Debug(name='Create-category')
    def __call__(self, request):

        if request['method'] == 'POST':
            data = request['request_params']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html',
                                    urls=request.get('urls', None),
                                    objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    urls=request.get('urls', None),
                                    objects_list=categories)


@AppRoute(routers=routers, url='/copy-course/')
class CopyCourse:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('course_list.html',
                                    objects_list=site.courses,
                                    name=new_course.category.name,
                                    urls=request.get('urls', None),
                                    )
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoute(routers=routers, url='/student-list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'

    def __call__(self, *args, **kwargs):
        logger.log('Список студенков')
        return super().__call__(*args)

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


@AppRoute(routers=routers, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_object(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


@AppRoute(routers=routers, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self, context, **kwargs):
        context = super().get_context_data(context)
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_object(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@AppRoute(routers=routers, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
