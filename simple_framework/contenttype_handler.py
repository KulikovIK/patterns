# запуск контроллера с передачей объекта request
def get_content(start_response, request, path, view):
    if path.endswith('.css/'):
        code, body = view(request, path.split('/')[-2])
        start_response(code, [('Content-Type', 'text/css')])
    else:
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
    return [body.encode('utf-8')]
