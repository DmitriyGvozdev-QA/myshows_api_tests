# Дальше мы будем тестировать ручку GET /series — получать свой список сериалов. Но чтобы ее протестировать, у нас должен быть этот список, то есть нам нужно подготовить тестовые данные. Напиши фикстуру, которая через библиотеку psycopg напрямую добавляет в базу данные, достаточные для проверки ручки GET /series. Не забудь, что данные должны удаляться после прохождения теста, таблицу можно очищать целиком.
# Напиши минимум один тест на ручку GET /series. Тест должен опираться на те данные, которые были ранее добавлены фикстурой, и обязательно должен успешно запускаться при вводе в консоли команды pytest в директории с тестовым проектом (то есть с твоим кодом, а не тестируемым сервисом).

from http import HTTPStatus

import allure
import psycopg
import pytest
from jsonschema import validate
from psycopg.rows import dict_row

from config.api_config import BASE_URL
from conftest import api_session
from helpers.utils import load_yml

SCHEMA = load_yml("get_series.yml")

@allure.title("Получение списка сериалов")
@pytest.mark.parametrize(
    "prepare_series_data",
    ["series_0", "series_1", "series_3"],
    indirect=True,
    ids=["0 rows", "1 row", "3 rows"]
)
def test__get_series(prepare_series_data, api_session):
    with allure.step("Получаем список сериалов из API"):
        response = api_session.get(
         BASE_URL + "/v1/series",
        )
    with allure.step("Проверяем код ответа"):
        assert response.status_code == 200, ''
    with allure.step("Проверяем тело ответа"):
        body = response.json()
        validate(instance=body, schema=SCHEMA)

        actual_count = len(body)
        expected_count = prepare_series_data
        assert actual_count == expected_count, \
            f"Expected {expected_count} series, got {actual_count}"


# [9.3][Практика] Параметризованные тесты

# Задание 1. Параметризация теста
# Напиши очередной тест на проект My Shows — в этот раз на метод PUT /api/v1/series/{id}. Запрос к этой ручке имеет несколько полей (смотри Swagger). Нужно написать параметризованный тест (т.е. всего одну тестовую функцию), который будет проверять изменение всех этих полей по отдельности (то есть при запуске должно получаться 5 тестов — по числу полей в теле запроса).
# Соответственно, шаги могут быть такими:
# В рамках сетапа фикстуры добавь сериал (лучше всего напрямую в базу, готовим тестовые данные).
# В тесте сделай запрос /api/v1/series/{id} с обновлением информации в каком-либо из полей.
# Посмотри в базу и убедись, что это поле действительно изменилось.
# В рамках тирдауна фикстуры верни таблицу в исходное состояние, то есть удали эту запись (в этот раз нужно удалить только данную конкретную запись, а не чистить всю таблицу).


@allure.title("Обновление информации о сериале")
@pytest.mark.parametrize(
    "field, new_value",
    [
        ("name", "Игра престолов"),
        ("photo", "https://avatars.mds.yandex.net/get-ott/223007/2a0000016ffbfaa9040ccd53e970ea7e086a/300x450"),
        ("rating", 10),
        ("status", "will_watch"),
        ("review", "зер гут"),
    ],
    ids=["name", "photo", "rating", "status", "review"]
)
def test__put_series(prepare_one_episode, field, new_value, api_session):
    series_id = prepare_one_episode
    with allure.step("Подключаемся к базе данных"):
        conn_params = {
            "dbname": "my-shows-rating",
            "user": "postgres",
            "password": "123456",
            "host": "127.0.0.1",
            "port": 5432,
        }
    with allure.step("Ищем в базе данных сериал по id"):
        with psycopg.connect(**conn_params, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM public.series WHERE id = %s;", (series_id,))
                current_data = cur.fetchone()

        payload = dict(current_data)
        payload[field] = new_value
    with allure.step("Получаем id сериала из API"):
        response = api_session.put(
            BASE_URL + f"/v1/series/{series_id}",
            json=payload
        )
    with allure.step("Проверяем код ответа"):
        body = response.json()
        assert response.status_code == HTTPStatus.OK, body
    with allure.step("Проверяем в базе данных, что информация о сериале обновилась"):
        with psycopg.connect(**conn_params, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM public.series WHERE id = %s;", (series_id,))
                row = cur.fetchone()
                assert row[field] == new_value


# Задание 2. Параметризация фикстуры
# К прошлому уроку ты написал тест, проверяющий ответ сервиса My Shows на запрос в ручку GET /series. В этом задании нужно расширить этот тест — сделать два разных набора сериалов, которые будут помещаться в базу в рамках сетапа фикстуры.
# Cделай непрямую параметризацию фикстуры (параметр indirect=True у декоратора pytest.mark.parametrize).
# В качестве параметра укажи файл, из которого будет браться скрипт SQL (текст скрипта можно сохранить в виде обычного файла New - File с расширением .sql, этот файл можно положить в папку data).
# Фикстура должна обработать имя файла, открыть его и загрузить его содержимое в базу.
# Затем фикстура должна вернуть количество строк, добавленных в базу.
# В тесте должен делаться запрос к ручке GET /series, а тело ответа проверяться на предмет совпадения количества строк с тем, что вернула фикстура.
# Также нужно проверять ответ на предмет совпадения со схемой (JSON schema).
# После прохождения каждого теста, как и раньше, нужно очищать таблицу с сериалами.
# Сделайте три проверки: какой будет ответ, если в базе будет 0 строк, 1 строка и 3 строки, то есть в итоге должна быть одна тестовая функция, выполняющаяся три раза с разными параметрами.
# Советы и рекомендации
# Для случая, когда строк 0, никаких данных в таблицу помещать не нужно, так что этот случай нужно обработать в фикстуре отдельно. И не забудь, что атрибута request.param может и не быть, поэтому нужно обработать такой случай.
