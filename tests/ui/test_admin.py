import time

import allure
import pytest
from pages.admin_page import AdminPage
from pages.login_page import LoginPage
from test_data.users import ADMIN, CHARLI

@allure.feature("Отображение страницы")
@allure.title("Проверка корректного отображения страницы Admin")
def test_admin_page_displayed(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    admin_page = AdminPage(driver)
    admin_page.open()
    admin_page.click(admin_page.SIDEBAR_ADMIN_PANEL)
    admin_page.assert_admin_page_is_opened()

@allure.feature("Удаление пользователя")
@allure.title("Проверка корректного отображения окна подтверждения удаления пользователя")
def test_confirm_user_delete_is_displayed(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    admin_page = AdminPage(driver)
    admin_page.open()
    admin_page.click(admin_page.SIDEBAR_ADMIN_PANEL)

    search_input = driver.find_element(*admin_page.SEARCH_USERS)
    search_input.clear()
    search_input.send_keys("bob_user")
    time.sleep(1)

    delete_buttons = driver.find_elements(*admin_page.DELETE_USER_BUTTON)
    delete_buttons[0].click()
    admin_page.assert_confirm_delete_user_is_opened()

@allure.title("Проверка отсутствия доступа к панели администратора у обычного пользователя")
def test_admin_page_not_displayed(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(CHARLI)

    admin_page = AdminPage(driver)
    admin_page.open()
    admin_page.no_admin_access_for_users()

@allure.feature("Поиск пользователя")
@allure.title("Проверка поиска пользователя по имени")
@pytest.mark.parametrize("search_text, expected_results", [
    ("bob_user", ["bob_user"]),
    ("charlie", ["charlie"]),
    ("guest1", ["guest1"]),
    ("admin", ["admin", "alice_admin"]),
    ("in", ["admin", "alice_admin"]),
    ("DIANA", ["diana"]),
], ids = [
    "полное совпадение с нижним подчёркиванием",
    "полное совпадение",
    "полное совпадение с цифрой",
    "частичное совпадение",
    "частичное совпадение в середине имени пользователя",
    "поиск с использованием верхнего регистра"
])
def test_search_by_username(driver, search_text, expected_results):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    admin_page = AdminPage(driver)
    admin_page.open()
    admin_page.driver.find_element(*admin_page.SIDEBAR_ADMIN_PANEL).click()
    time.sleep(1)
    search_results = admin_page.find_users_by_usernames(search_text)
    assert sorted(search_results) == sorted(expected_results)

@allure.feature("Поиск пользователя")
@allure.title("Проверка поиска пользователя по email")
@pytest.mark.parametrize("search_text, expected_results", [
    ("admin@example.com", ["admin@example.com"]),
    ("diana", ["diana@example.com"]),
    ("guest", ["guest1@example.com", "guest2@example.com"]),
    ("ALICE", ["alice@example.com"]),
], ids = [
    "полное совпадение",
    "только первая часть",
    "частичное совпадение",
    "поиск с использованием верхнего регистра"
])
def test_search_by_email(driver, search_text, expected_results):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    admin_page = AdminPage(driver)
    admin_page.open()
    admin_page.driver.find_element(*admin_page.SIDEBAR_ADMIN_PANEL).click()
    search_results = admin_page.find_users_by_emails(search_text)
    assert sorted(search_results) == sorted(expected_results)

@allure.feature("Поиск пользователя")
@allure.title("Негативная проверка поиска пользователей")
@pytest.mark.parametrize("search_text", [
    "user_that_does_not_exists",
    " ",
    "a-d-m-i-n",
], ids = [
    "несуществующий пользователь",
    "пробелы",
    "альтернативное написание",
])
def test_search_users_negative(driver, search_text):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    admin_page = AdminPage(driver)
    admin_page.open()
    admin_page.driver.find_element(*admin_page.SIDEBAR_ADMIN_PANEL).click()
    admin_page.find_users_by_emails(search_text)
    admin_page.assert_element_visible(admin_page.NO_RESULTS_MESSAGE)

@allure.feature("Удаление пользователя")
@allure.title("Проверка корректного удаления пользователя по имени")
def test_user_is_deleted(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    admin_page = AdminPage(driver)
    admin_page.open()
    admin_page.delete_user_by_username("bob_user")

    admin_page.find_users_by_usernames("bob_user")
    admin_page.assert_element_visible(admin_page.NO_RESULTS_MESSAGE)



