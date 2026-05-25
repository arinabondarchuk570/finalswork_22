import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from test_data.users import User
from selenium.webdriver.support import expected_conditions as EC

class LoginPage(BasePage):
    LOGIN_INPUT = (By.ID, 'id-input-login-email-input')
    PASSWORD_INPUT = (By.ID, 'id-input-login-password-input')
    SUBMIT = (By.XPATH, '//*[@data-qa="login-submit-button"]')
    REGISTER_REDIRECT = (By.CSS_SELECTOR, 'a[href="/register"]')
    LOGIN_MESSAGE = (By.CSS_SELECTOR, ".toast-message")

    def __init__(self, driver):
        self.url = '/login'

        super().__init__(driver, self.url)
        self.driver: WebDriver = driver

    @allure.step("Войти в систему")
    def login(self, user: User):
        self.send_keys(self.LOGIN_INPUT, user.email)
        self.send_keys(self.PASSWORD_INPUT, user.password)

        self.click(self.SUBMIT)
        self.wait.until(EC.url_contains("/dashboard"))

    @allure.step("Войти в систему")
    def login_neg(self, user: User):
        self.send_keys(self.LOGIN_INPUT, user.email)
        self.send_keys(self.PASSWORD_INPUT, user.password)

        self.click(self.SUBMIT)

    @allure.step("Переход на страницу регистрации")
    def registration_redirect(self):
        self.click(self.REGISTER_REDIRECT)

    @allure.step("Видимость toast-сообщения")
    def toast_message_is_visible(self):
        self.assert_element_visible(self.LOGIN_MESSAGE)
        return True

    @allure.step("Получить текст toast-сообщения")
    def get_toast_message_text(self):
        toast = self.driver.find_element(*self.LOGIN_MESSAGE)
        return toast.text
