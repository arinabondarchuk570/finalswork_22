import allure
import time
from conftest import api_admin


@allure.title("Регистрация и удаление пользователя через API")
def test_register_user_via_api(api_admin):
    unique_user_id = int(time.time())
    username = f"api_user_{unique_user_id}"
    email = f"api_{unique_user_id}@example.com"

    payload = {
        "username": username,
        "email": email,
        "password": "Password123!",
        "password_confirm": "Password123!"
    }

    reg_response = api_admin.post("/api/auth/register", data=payload)
    assert reg_response.status_code == 201, "Пользователь не зарегистрирован"

    response_data = reg_response.json()
    assert "access_token" in response_data, "Токен не получен"

    token = response_data["access_token"]
    user_id = api_admin.get_user_id_from_token(token)
    assert user_id is not None, "Не удалось получить ID из токена"

    delete_response = api_admin.delete(f"/api/users/{user_id}")
    assert delete_response.status_code in [200, 204]
    get_response = api_admin.get(f"/api/users/{user_id}", expected_status=404)
    assert get_response.status_code in [404]
