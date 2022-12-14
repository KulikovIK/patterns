import abc
import copy
import quopri
from .behavioral_patterns import Subject

class User:
    def __init__(self, name):
        self.name = name


class Teacher(User):
    pass


class Student(User):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_is, name):
        return cls.types.get(type_is)(name)


class CoursePrototype:
    # прототип курсов обучения

    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types.get(type_)(name, category)


class Catalog(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def list_children(self):
        pass


class Category(Catalog):
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.categories = {}
        self._children = []
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result

    def list_children(self):
        return self._children

    def append(self, cls):
        if isinstance(cls, Catalog):
            self._children.append(cls)


class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def find_category_by_id(self, id):
        for category in self.categories:
            print(f'category: {category}')
            if category.id == id:
                return category
        raise Exception(f'There`s no such category with id={id}')

    def get_course(self, name):
        for course in self.courses:
            if course.name == name:
                return course
        return None

    def get_student(self, name) -> Student:
        for student in self.students:
            if student.name == name:
                return student

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')
