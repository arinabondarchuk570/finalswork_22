import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RegistrationPage(BasePage):
    LOGIN_BUTTON = (By.CSS_SELECTOR, '.auth-form-link')
    REGISTER_BUTTON = (By.CSS_SELECTOR, '[data-qa="register-submit-button"]')
    NAME_INPUT = (By.CSS_SELECTOR, '[data-qa="register-username-input"]')
    EMAIL_INPUT = (By.CSS_SELECTOR, '[data-qa="register-email-input"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '[data-qa="register-password-input"]')
    CONFIRM_PASSWORD_INPUT = (By.CSS_SELECTOR, '[data-qa="register-confirm-password-input"]')

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.url = '/register'

        super().__init__(driver, self.url)

    @allure.step("Регистрация пользователя")
    def register(self, User):
        self.send_keys(self.NAME_INPUT, User.name)
        self.send_keys(self.EMAIL_INPUT, User.email)
        self.send_keys(self.PASSWORD_INPUT, User.password)
        self.send_keys(self.CONFIRM_PASSWORD_INPUT, User.password)
        self.click(self.REGISTER_BUTTON)

    @allure.step("Получить сообщение валидации для email")
    def get_email_validation_message(self):
        email_field = self.driver.find_element(*self.EMAIL_INPUT)
        return self.driver.execute_script("return arguments[0].validationMessage;", email_field)

    @allure.step("Проверить, что открыта страница регистрации")
    def assert_registration_page_opened(self):
        self.assert_element_visible(self.NAME_INPUT)
        self.assert_element_visible(self.EMAIL_INPUT)
        self.assert_element_visible(self.PASSWORD_INPUT)
        self.assert_element_visible(self.CONFIRM_PASSWORD_INPUT)
