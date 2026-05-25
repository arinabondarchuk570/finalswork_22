import allure
import time

@allure.feature("API Доски")
@allure.title("Создание доски через API")
def test_create_board_via_api(api_admin, driver):
    board_title = f"Новая доска API {int(time.time())}"
    response = api_admin.post("/api/boards/", {
        "title": board_title,
        "description": "Тест создание доски через API",
        "public": True
    })
    assert response.status_code == 201
    board_data = response.json()
    assert board_data["title"] == board_title
    assert board_data["description"] == "Тест создание доски через API"
    assert board_data["public"] == True
    assert "id" in board_data

    api_admin.delete(f"/api/boards/{board_data['id']}")

@allure.feature("API Доски")
@allure.title("Удаление доски через API")
def test_delete_board_via_api(api_admin):
    board_title = f"Тест удаление доски {int(time.time())}"
    response = api_admin.post("/api/boards/", {"title": board_title})
    board_id = response.json()["id"]

    api_admin.delete(f"/api/boards/{board_id}")
    api_admin.get(f"/api/boards/{board_id}", expected_status=404)
