import json
import requests
from mimesis.locales import Locale
from mimesis.enums import Gender
from mimesis import Person


# В этой функции хранятся базовый url адрес и заголовки.
def get_url_data():

    base_url = 'https://petstore.swagger.io/v2'
    base_headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

    return base_url, base_headers


# Функция формирует набор тестовых данных для добавления пользователя используя библиотеку mimesis.
def generate_person():

    gender = Person().random.choice([Gender.MALE, Gender.FEMALE])
    person_id = Person().random.randint(1, 999999999)
    user_name = Person(Locale.EN).username('ld')
    first_name = Person(Locale.RU).first_name(gender)
    last_name = Person(Locale.RU).last_name(gender)
    e_mail = Person(Locale.EN).email()
    password = Person(Locale.EN).password()
    phone_number = Person().telephone(mask='+7(###)-###-##-##')
    user_status = Person().random.randint(0, 1)

    return {
        'id': person_id,
        'user_name': user_name,
        'first_name': first_name,
        'last_name': last_name,
        'e_mail': e_mail,
        'password': password,
        'phone_number': phone_number,
        'user_status': user_status
    }


# Функция отправляет запрос на добавление пользователя с набором тестовых данных.
def create_user(url, header, data):

    func_data = {
        "id": data.get('id'),
        "username": data.get('user_name'),
        "firstName": data.get('first_name'),
        "lastName": data.get('last_name'),
        "email": data.get('e_mail'),
        "password": data.get('password'),
        "phone": data.get('phone_number'),
        "userStatus": data.get('user_status')
    }

    create_user_response = requests.post(url=f'{url}/user', headers=header, json=func_data)

    if create_user_response.status_code == 200:
        try:
            status = create_user_response.status_code
            message = create_user_response.json()
        except requests.exceptions.JSONDecodeError:
            status = create_user_response.status_code
            message = create_user_response.text
    else:
        status = create_user_response.status_code
        message = create_user_response.text

    return status, message, func_data


# Функция получает данные пользователя по его имени пользователя.
def get_user_by_username(url, header, username):

    get_user_response = requests.get(url=f'{url}/user/{username}', headers=header)
    if get_user_response.status_code == 200:
        try:
            status = get_user_response.status_code
            message = get_user_response.json()
        except requests.exceptions.JSONDecodeError:
            status = get_user_response.status_code
            message = get_user_response.text
    else:
        status = get_user_response.status_code
        message = get_user_response.text

    return status, message


# Функция по имени пользователя позволяет изменить его данные, за исключением id и username.
def update_user(url, header, username, old_data, new_data):

    upd_user_info = {
        "id": old_data.get('id'),
        "username": old_data.get('user_name'),
        "firstName": new_data.get('first_name'),
        "lastName": new_data.get('last_name'),
        "email": new_data.get('e_mail'),
        "password": new_data.get('password'),
        "phone": new_data.get('phone_number'),
        "userStatus": new_data.get('user_status')
    }

    upd_user_response = requests.put(url=f'{url}/user/{username}', headers=header, json=upd_user_info)
    if upd_user_response.status_code == 200:
        try:
            status = upd_user_response.status_code
            message = upd_user_response.json()
        except requests.exceptions.JSONDecodeError:
            status = upd_user_response.status_code
            message = upd_user_response.text
    else:
        status = upd_user_response.status_code
        message = upd_user_response.text

    return status, message


# Функция позволяет удалить пользователя по его имени пользователя.
def delete_user(url, header, username):

    del_user_response = requests.delete(url=f'{url}/user/{username}', headers=header)
    if del_user_response.status_code == 200:
        try:
            status = del_user_response.status_code
            message = del_user_response.json()
        except requests.exceptions.JSONDecodeError:
            status = del_user_response.status_code
            message = del_user_response.text
    else:
        status = del_user_response.status_code
        message = del_user_response.text

    return status, message


# Основная функция для использования методов работы с пользовательскими данными.
def main():
    # Задаем url и заголовки для формирования запроса, формируем данные тестового пользователя и данные для изменения.
    host, headers = get_url_data()
    generate_new_user = generate_person()
    user_data_rename = generate_person()

    # Добавляем нового пользователя на сервер
    add_new_user = create_user(url=host, header=headers, data=generate_new_user)

    # Выводим на печать статус код и ответ на запрос.
    print(f'Добавление нового пользователя {generate_new_user.get("user_name")} на сервер:\n'
          f'Статус запроса: {add_new_user[0]}\n'
          f'Ответ на запрос: {json.dumps(add_new_user[1], indent=4, sort_keys=False, ensure_ascii=False)}\n')

    # По username пользователя получаем его данные.
    get_user_info = get_user_by_username(url=host, header=headers, username=add_new_user[2].get('username'))

    # Выводим на печать статус код и prettyprint ответа на запрос.
    print(f'Получение данных пользователя {add_new_user[2].get("username")}:\nСтатус запроса: {get_user_info[0]}\n'
          f'Ответ на запрос: {json.dumps(get_user_info[1], indent=4, sort_keys=False, ensure_ascii=False)}\n')

    # По username изменяем данные существующего пользователя.
    add_update_user = update_user(url=host, header=headers, username=get_user_info[1].get('username'),
                                  old_data=generate_new_user, new_data=user_data_rename)

    # Выводим на печать статус код и prettyprint ответа на запрос.
    print(f'Обновление данных пользователя {get_user_info[1].get("username")}:\nСтатус запроса: {add_update_user[0]}\n'
          f'Ответ на запрос: {json.dumps(add_update_user[1], indent=4, sort_keys=False, ensure_ascii=False)}\n')

    # По username удаляем существующего пользователя
    del_user = delete_user(url=host, header=headers, username=add_new_user[2].get('username'))

    # Выводим на печать статус код и prettyprint ответа на запрос.
    print(f'Получение данных об операции удаления пользователя {add_new_user[2].get("username")}:\n'
          f'Статус запроса: {del_user[0]}\n'
          f'Ответ на запрос: {json.dumps(del_user[1], indent=4, sort_keys=False, ensure_ascii=False)}')


if __name__ == '__main__':
    main()
