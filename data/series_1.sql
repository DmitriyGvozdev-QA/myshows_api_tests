INSERT INTO public.series (id, "name", photo, rating, status, review)
VALUES (101, 'Перерождение', 'https://avatars.mds.yandex.net/get-kinopoisk-image/1773646/e7668e01-e148-4c5e-9d25-6769be1559f5/600x900', 6, 'watching', 'плохой')
RETURNING id;