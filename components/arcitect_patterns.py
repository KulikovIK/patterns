from threading import local


class UnitOfWork:
    cur_thread = local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def set_mapper_register(self, register):
        self.MapperRegister = register

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def insert(self):
        for obj in self.new_objects:
            self.MapperRegister.get_mapper(obj).insert(obj)

    def update(self):
        for obj in self.dirty_objects:
            self.MapperRegister.get_mapper(obj).update(obj)

    def delete(self):
        for obj in self.removed_objects:
            self.MapperRegister.get_mapper(obj).delete(obj)

    def commit(self):
        self.insert()
        self.update()
        self.delete()

        self.new_objects.clear()
        self.dirty_objects.clear()
        self.removed_objects.clear()

    @staticmethod
    def new_thread():
        __class__.set_thread(UnitOfWork())

    @classmethod
    def set_thread(cls, unit_of_work):
        cls.cur_thread.unit_of_work = unit_of_work

    @classmethod
    def get_thread(cls):
        return cls.cur_thread.unit_of_work


class DomainObject:

    def mark_new(self):
        UnitOfWork.get_thread().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_thread().register_dirty(self)

    def mark_remove(self):
        UnitOfWork.get_thread().register_removed(self)
