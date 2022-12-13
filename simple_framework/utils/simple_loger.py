def print_log(method: str, params: dict) -> None:
    log_string = f'Поступил {method} запрос с параметрами: {params}'
    # print(log_string)
    with open('log_file.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(log_string + '\n')
