from simple_framework.main import Framework


class FakeServer(Framework):
    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
