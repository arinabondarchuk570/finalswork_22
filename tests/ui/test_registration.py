import allure
import time
from pages.registration_page import RegistrationPage
from test_data.users import User

@allure.feature("Регистрация")
@allure.title("Успешная регистрация нового пользователя")
def test_successful_registration(driver):
    unique_id = int(time.time())
    username = f"user_{unique_id}"
    email = f"test_{unique_id}@example.com"
    password = "Password123!"

    registration_page = RegistrationPage(driver)
    registration_page.open()

    new_user = User(name=username, email=email, password=password)
    registration_page.register(new_user)
    time.sleep(2)

    assert "/dashboard" in driver.current_url

@allure.title("Проверка валидации некорректного Email")
def test_registration_invalid_email(driver):
    registration_page = RegistrationPage(driver)
    registration_page.open()

    username = f"testuser"
    email = f"invalid-email-no-at"
    password = "Password123!"

    new_user = User(name=username, email=email, password=password)
    registration_page.register(new_user)

    assert registration_page.get_email_validation_message()

@allure.title("Проверка отображения страницы регистрации")
def test_registration_page_is_opened(driver):
    registration_page = RegistrationPage(driver)
    registration_page.open()
    registration_page.assert_registration_page_opened()
