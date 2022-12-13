class BaseRequest:
    @staticmethod
    def parse_input_data(data: str) -> dict:
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                # выделение ключа и значения
                k, v = item.split('=')
                result[k] = v
        return result


# get запрос
class GetRequests(BaseRequest):

    @staticmethod
    def get_request_params(environ: dict) -> dict:
        # получаем параметры запроса
        query_string = environ.get('QUERY_STRING')
        # получение словаря параметров запроса
        request_params = GetRequests.parse_input_data(query_string)
        return request_params


# post запрос
class PostRequests(BaseRequest):
    @staticmethod
    def get_wsgi_input_data(environ: dict) -> bytes:
        # получение длины тела
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        # print(content_length)

        return environ.get('wsgi.input').read(content_length) if content_length else b''

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            # декодирование данных
            decoded_data = data.decode(encoding='utf-8')
            # print(f'строка после декодирования - {decoded_data}')
            result = PostRequests.parse_input_data(decoded_data)
        return result

    def get_request_params(self, environ: dict) -> dict:
        # получение данных
        request_params = self.get_wsgi_input_data(environ)
        request_params = self.parse_wsgi_input_data(request_params)
        return request_params
