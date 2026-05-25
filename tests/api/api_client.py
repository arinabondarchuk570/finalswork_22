import allure
import json

import jwt
import requests


class ApiClient:
    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    @allure.step("API POST")
    def post(self, endpoint, data, expected_status=201):
        url = f"{self.base_url}{endpoint}"
        response = requests.post(
            url,
            data=json.dumps(data),
            headers=self.headers
        )
        assert response.status_code == expected_status
        return response

    @allure.step("API DELETE")
    def delete(self, endpoint, expected_statuses=[200, 204]):
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, headers=self.headers)
        assert response.status_code in expected_statuses
        return response

    @allure.step("API GET")
    def get(self, endpoint, expected_status=200):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers)
        assert response.status_code == expected_status
        return response

    @allure.step("GET JSON")
    def get_json(self, endpoint, expected_status=200):
        response = self.get(endpoint, expected_status)
        return response.json()

    @allure.step("Получить id пользователя из jwt токена")
    def get_user_id_from_token(self, token):
        try:
            decoded = jwt.decode(token, options={"verify_signature": False})
            return decoded.get('sub') or decoded.get('user_id') or decoded.get('id')
        except Exception as e:
            print(f"Ошибка декодирования: {e}")
            return None

