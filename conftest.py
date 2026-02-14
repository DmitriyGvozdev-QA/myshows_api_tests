import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
import pytest
import requests

load_dotenv()



# [9.2][Практика] Pytest фикстуры


@pytest.fixture()
def prepare_series_data(request):
    conn_params = {
        "dbname": "my-shows-rating",
        "user": "postgres",
        "password": "123456",
        "host": "127.0.0.1",
        "port": 5432,
    }

    conn = psycopg.connect(**conn_params, row_factory=dict_row)
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM public.series;")
            sql_filename = request.param
            sql_path = os.path.join("data", f"{sql_filename}.sql")

            inserted_count = 0

            if os.path.exists(sql_path):
                with open(sql_path, "r", encoding="utf-8") as f:
                    sql = f.read()

                if sql:
                    cur.execute(sql)
                    if cur.description:
                        rows = cur.fetchall()
                        inserted_count = len(rows)
                    else:
                        cur.execute("SELECT COUNT(*) FROM public.series;")
                        inserted_count = cur.fetchone()[0]

                conn.commit()

        yield inserted_count  # ← возвращаем количество добавленных строк

#после теста очищаем таблицу в БД
    finally:
        with conn.cursor() as cur:
                cur.execute("DELETE FROM public.series;")
                conn.commit()
                conn.close()




# [9.3][Практика] Параметризованные тесты

# Задание 1. Параметризация теста
# Напиши очередной тест на проект My Shows — в этот раз на метод PUT /api/v1/series/{id}. Запрос к этой ручке имеет несколько полей (смотри Swagger). Нужно написать параметризованный тест (т.е. всего одну тестовую функцию), который будет проверять изменение всех этих полей по отдельности (то есть при запуске должно получаться 5 тестов — по числу полей в теле запроса).
# Соответственно, шаги могут быть такими:
# В рамках сетапа фикстуры добавь сериал (лучше всего напрямую в базу, готовим тестовые данные).
# В тесте сделай запрос /api/v1/series/{id} с обновлением информации в каком-либо из полей.
# Посмотри в базу и убедись, что это поле действительно изменилось.
# В рамках тирдауна фикстуры верни таблицу в исходное состояние, то есть удали эту запись (в этот раз нужно удалить только данную конкретную запись, а не чистить всю таблицу).



@pytest.fixture()
def prepare_one_episode():
    conn_params = {
        "dbname": "my-shows-rating",
        "user": "postgres",
        "password": "123456",
        "host": "127.0.0.1",
        "port": 5432,
    }

    conn = psycopg.connect(**conn_params, row_factory=dict_row)

    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM public.series WHERE id = 6;")
            cur.execute("""
                INSERT INTO public.series (id, name, photo, rating, status, review)
                VALUES
                    (6, 'Друзья', 'https://avatars.mds.yandex.net/get-kinopoisk-image/4486454/bae692d9-8260-46a4-9188-8509a72aa005/300x450', 9, 'watching', 'отлично')
                    RETURNING id;
            """)
            result = cur.fetchone()
            series_id = result["id"]
            conn.commit()

        yield series_id   #передаем series_id в сам тест

    finally:    # после теста очищаем эту строку с сериалом в БД

        with conn.cursor() as cur:
            cur.execute("DELETE FROM public.series WHERE id = %s;", (series_id,))
            conn.commit()

        conn.close()


#Для построения отчета в Аллюре
from helpers.api_helpers import ApiSession

@pytest.fixture(scope="session")
def api_session():
    with requests.Session() as s:
        yield ApiSession(s)