import allure
import pytest
from pages.boards_page import BoardsPage
from pages.login_page import LoginPage
from test_data.users import ADMIN

@allure.feature("Отображение страницы")
@allure.title("Проверка отображения страницы Boards")
def test_boards_page_display(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    boards_page = BoardsPage(driver)
    boards_page.open()
    boards_page.assert_boards_page_opened()

@allure.title("Проверка наличия досок у пользователя")
def test_user_has_boards(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    boards_page = BoardsPage(driver)
    boards_page.open()
    boards_count = boards_page.get_number_of_boards()
    assert boards_count > 0, \
        f"Найдено досок: {boards_count}"
    print(f"У пользователя найдено досок: {boards_count}")

@allure.title("Проверка отсутствия досок у пользователя")
@pytest.mark.xfail
def test_user_has_no_boards(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    boards_page = BoardsPage(driver)
    boards_page.open()
    boards_count = boards_page.get_number_of_boards()
    assert boards_count == 0, \
        f"Найдено: {boards_count}"
    print(f"У пользователя нет досок")

@allure.feature("Поиск досок")
@allure.title("Поиск досок по названию")
@pytest.mark.parametrize("search_text, expected_results", [
    ("Техническая поддержка", ["Техническая Поддержка"]),
    ("проект", ["Проект Разработка", "Архивные Проекты"]),
    ("инг", ["Маркетинг и Продвижение"]),
    ("АРХИВНЫЕ ПРОЕКТЫ", ["Архивные Проекты"]),
])
def test_search_for_boards(driver, search_text, expected_results):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    boards_page = BoardsPage(driver)
    boards_page.open()
    search_results = boards_page.search_boards_by_name(search_text)
    assert sorted(set(search_results)) == sorted(expected_results)

@allure.feature("Поиск досок")
@allure.title("Негативная проверка поиска досок")
@pytest.mark.parametrize("search_text", [
    "Board that does not exist",
    "  ",
])
def test_search_boards_negative(driver, search_text):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    boards_page = BoardsPage(driver)
    boards_page.open()
    boards_page.search_boards_by_name(search_text)
    boards_page.assert_element_visible(boards_page.NO_BOARDS_FOUND)

@allure.feature("Поиск досок")
@allure.title('Проверка поиска досок с фильтром "Только публичные"')
@pytest.mark.parametrize("search_text, expected_results", [
    ("публичный roadmap", ["Публичный Roadmap"]),
])
def test_search_boards_with_public_toggle(driver, search_text, expected_results):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    boards_page = BoardsPage(driver)
    boards_page.open()
    boards_page.filter_public_boards_only()
    search_results = boards_page.search_boards_by_name(search_text)
    boards_page.assert_board_is_public()
    assert search_results == expected_results

@allure.feature("Создание досок")
@allure.title("Проверка корректного отображения окна создания новой доски")
def test_create_board_is_opened(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    boards_page = BoardsPage(driver)
    boards_page.open()
    boards_page.click(boards_page.CREATE_BOARD_BUTTON)
    boards_page.assert_create_board_opened()

@allure.feature("Создание досок")
@allure.title("Негативная проверка создания доски без названия")
def test_create_board_negative(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    boards_page = BoardsPage(driver)
    boards_page.open()
    boards_page.click(boards_page.CREATE_BOARD_BUTTON)
    boards_page.click(boards_page.SUBMIT_NEW_BOARD)
    title_input = driver.find_element(*boards_page.CREATE_BOARD_TITLE_INPUT)

    validation_message = driver.execute_script("return arguments[0].validationMessage;", title_input)
    assert any(word in validation_message.lower() for word in ["заполните"])

@allure.feature("Создание досок")
@allure.title("Позитивная проверка создания доски")
@pytest.mark.parametrize("title_text, description_text, is_public", [
    ("Новая публичная доска", "Описание", True),
    ("Новая приватная доска", "Описание", False),
])
def test_create_board(driver, title_text, description_text, is_public):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    boards_page = BoardsPage(driver)
    boards_page.open()
    boards_page.create_board(title_text, description_text, is_public)
    boards_page.assert_element_visible(boards_page.BOARD_CREATED)
    success_message = driver.find_element(*boards_page.BOARD_CREATED)
    assert success_message.is_displayed()





