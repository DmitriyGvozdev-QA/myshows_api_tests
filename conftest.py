import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
import pytest

load_dotenv()

@pytest.fixture()
def prepare_series_data():
    conn_params = {
        "dbname": "my-shows-rating",
        "user": "postgres",
        "password": "123456",
        "host": "127.0.0.1",
        "port": 5432,
    }

    conn = psycopg.connect(**conn_params, row_factory=dict_row)

    with conn.cursor() as cur:
        cur.execute("DELETE FROM public.series;")
        cur.execute("""
            INSERT INTO public.series (id, "name", photo, rating, status, review)
            VALUES
                (1, 'Интерстеллар', 'https://avatars.mds.yandex.net/get-kinopoisk-image/1600647/430042eb-ee69-4818-aed0-a312400a26bf/72x108', 8, 'watching', 'отлично'),
                (2, 'Побег из Шоушенка', 'https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/0b76b2a2-d1c7-4f04-a284-80ff7bb709a4/72x108', 8, 'watching', 'отлично'),
                (3, 'Бойцовский клуб', 'https://avatars.mds.yandex.net/get-kinopoisk-image/16490236/495fb59a-bff1-4626-baba-bb392fede945/72x108', 8, 'watching', 'отлично'),
                (4, 'Начало', 'https://avatars.mds.yandex.net/get-kinopoisk-image/1629390/8ab9a119-dd74-44f0-baec-0629797483d7/72x108', 8, 'watched', 'Отличный фильм'),
                (5, 'Помпеи', 'https://avatars.mds.yandex.net/get-kinopoisk-image/9784475/6d794b5f-b072-4336-8ba4-0a9142f40b6d/72x108', 6, 'watched', 'Так себе');
        """)
        conn.commit()

    yield  #тут переходим в тест и выполняем его

#после теста очищаем таблицу в БД
    with conn.cursor() as cur:
        cur.execute("DELETE FROM public.series;")
        conn.commit()

    conn.close()