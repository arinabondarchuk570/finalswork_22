import allure
import pytest

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from test_data.users import CHARLI
from test_data.users import INVALID_EMAIL_USER, INVALID_PASSWORD_USER, EMPTY_EMAIL_USER, EMPTY_PASSWORD_USER

@allure.feature("Авторизация")
@allure.title("Проверка авторизации")
def test_login(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(CHARLI)

    dashboard_page = DashboardPage(driver)
    dashboard_page.assert_that_dashboard_opened()

@allure.title("Проверка перехода на страницу регистрации")
def test_registration_redirect(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.registration_redirect()

    expected_url = "/register"
    assert expected_url in driver.current_url

@allure.feature("Авторизация")
@allure.title("Негативная проверка авторизации")
@pytest.mark.parametrize("test_user, expected_result, error_type", [
    (INVALID_EMAIL_USER, "incorrect email or password", "toast"),
    (INVALID_PASSWORD_USER, "incorrect email or password", "toast"),
    (EMPTY_EMAIL_USER, "заполните это поле", "val_email"),
    (EMPTY_PASSWORD_USER, "заполните это поле", "val_password"),
], ids=[
    "Невалидный email",
    "Неверный пароль",
    "Пустое поле email",
    "Пустое поле с паролем",
])
def test_login_negative(driver, test_user, expected_result, error_type):
    login_page = LoginPage(driver)
    login_page.open()

    login_page.login_neg(test_user)
    if error_type == "toast":
        assert login_page.toast_message_is_visible()
        toast_text = login_page.get_toast_message_text()
        assert expected_result.lower() in toast_text.lower()
    elif error_type == "val_email":
        email_field = driver.find_element(*login_page.LOGIN_INPUT)
        validation_message = driver.execute_script("return arguments[0].validationMessage;", email_field)
        assert expected_result.lower() in validation_message.lower()
    elif error_type == "val_password":
        password_field = driver.find_element(*login_page.PASSWORD_INPUT)
        validation_message = driver.execute_script("return arguments[0].validationMessage;", password_field)
        assert expected_result.lower() in validation_message.lower()


