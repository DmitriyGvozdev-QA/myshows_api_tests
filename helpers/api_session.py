import json

import allure


class ApiSession:
    def __init__(self, session):
        self.session = session

    def _send(self, method, url, **kwargs):
        response = self.session.request(method=method, url=url, **kwargs)
        allure.attach(
            body=f"Request:\n"
                 f"URL: {url}\n"
                 f"Method: {method}\n"
                 f"Headers: {json.dumps(dict(response.request.headers), indent=2, ensure_ascii=False)}\n"
                 f"Body: {response.request.body or ''}\n\n"
                 f"Response:\n"
                 f"Status Code: {response.status_code}\n"
                 f"Headers: {json.dumps(dict(response.headers), indent=2, ensure_ascii=False)}\n"
                 f"Body: {response.text}",
            name="Детальная информация о запросе и ответе",
            attachment_type=allure.attachment_type.TEXT
        )
        return response

    @allure.step("GET-запрос к адресу {url}")
    def get(self, url, params=None, **kwargs):
        return self._send("GET", url=url, params=params, **kwargs)

    @allure.step("PUT-запрос к адресу {url}")
    def put(self, url, params=None, json=None, **kwargs):
        return self._send("PUT", url=url, params=params, json=json, **kwargs)
