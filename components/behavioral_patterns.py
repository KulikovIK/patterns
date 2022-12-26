from jsonpickle import dumps, loads


class Observer:

    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observers = []

    def notify(self):
        for observer in self.observers:
            observer.update(self)


class SmsNotifier(Observer):
    def update(self, subject):
        print(f'SMS-> к нам присоединился {subject.students[-1].name}')


class EmailNotifier(Observer):
    def update(self, subject):
        print(f'EMAIL-> к нам присоединился {subject.students[-1].name}')


class BaseSerializer:
    def __init__(self, object):
        self.object = object

    def save(self):
        return dumps(self.object)

    @staticmethod
    def load(data):
        return loads(data)



