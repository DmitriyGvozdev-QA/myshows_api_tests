INSERT INTO public.series (id, "name", photo, rating, status, review)
VALUES
	(210, 'Наследие', 'https://avatars.mds.yandex.net/get-kinopoisk-image/1898899/d1ff8038-5dc1-4b53-80c6-04f82186369f/600x900', 7, 'watching', 'норм'),
	(220, 'Настоящая кровь', 'https://avatars.mds.yandex.net/get-ott/1531675/2a0000016ffbf9c308ae27b7e0842ad79baa/600x900', 7, 'watching', 'норм'),
	(230, 'Сверхестественное', 'https://avatars.mds.yandex.net/get-kinopoisk-image/4303601/c2c45ca9-0270-4bb2-bb82-5de3f01effbc/600x900', 8, 'watching', 'хорошо')
	RETURNING id;