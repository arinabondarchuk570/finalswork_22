import time

import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from config import BaseConfig
from pages.base_page import BasePage


class AdminPage(BasePage):
    # Локаторы боковой панели
    SIDEBAR_ADMIN_PANEL = (By.CSS_SELECTOR, '[data-qa="sidebar-admin-link"]')
    #Локаторы заголовков
    ADMIN_H1 = (By.CSS_SELECTOR, '[class="admin-page-header"]')
    USER_HEADER = (By.XPATH, "//th[text()='Пользователь']")
    EMAIL_HEADER = (By.XPATH, "//th[text()='Email']")
    ROLE_HEADER = (By.XPATH, "//th[text()='Роль']")
    REG_DATE_HEADER = (By.XPATH, "//th[text()='Дата регистрации']")
    ACTIONS_HEADER = (By.XPATH, "//th[text()='Действия']")
    #Локаторы связанные с поиском
    SEARCH_USERS = (By.CSS_SELECTOR, '[data-qa="input"]')
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, ".admin-table-empty")
    #Локаторы таблицы пользователей
    ALL_USER_NAMES = (By.CSS_SELECTOR, '[class="admin-table-user-name"]')
    ALL_USER_EMAILS = (By.CSS_SELECTOR, '[class="admin-table-user-email"]')
    #Локаторы связанные с удалением пользователя
    DELETE_USER_BUTTON = (By.CSS_SELECTOR, '.btn.btn-danger')
    DELETE_CONFIRMATION_TITLE = (By.XPATH, "//h2[text()='Удалить пользователя']")
    CANCEL_DELETE_USER_BUTTON = (By.CSS_SELECTOR, '[data-qa="delete-user-cancel-button"]')
    CONFIRM_DELETE_USER_BUTTON = (By.CSS_SELECTOR, '[data-qa="delete-user-confirm-button"]')

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.url = "/admin"

        super().__init__(driver, self.url)

    @allure.step("Проверка отображения страницы Аdmin")
    def assert_admin_page_is_opened(self):
        self.assert_element_visible(self.ADMIN_H1)
        self.assert_element_visible(self.SEARCH_USERS)
        self.assert_element_visible(self.USER_HEADER)
        self.assert_element_visible(self.EMAIL_HEADER)
        self.assert_element_visible(self.ROLE_HEADER)
        self.assert_element_visible(self.REG_DATE_HEADER)
        self.assert_element_visible(self.ACTIONS_HEADER)

    @allure.step("Поиск пользователей по имени")
    def find_users_by_usernames(self, search_text):
        find_input = self.driver.find_element(*self.SEARCH_USERS)
        find_input.clear()
        find_input.send_keys(search_text)
        time.sleep(1)

        users_found = [name.text.lower() for name in self.driver.find_elements(*self.ALL_USER_NAMES)]

        return users_found

    @allure.step("Поиск пользователей по email")
    def find_users_by_emails(self, search_text):
        find_input = self.driver.find_element(*self.SEARCH_USERS)
        find_input.clear()
        find_input.send_keys(search_text)
        time.sleep(1)

        users_found = [email.text for email in self.driver.find_elements(*self.ALL_USER_EMAILS)]

        return users_found

    @allure.step("Проверка отсутствия доступа к страницe Admin у обычного пользователя")
    def no_admin_access_for_users(self):
        expected_url = f"{BaseConfig.ROOT_PATH}/dashboard"
        assert expected_url in self.driver.current_url

    @allure.step("Удаление пользователя")
    def delete_user_by_username(self, username):
        self.find_users_by_usernames(username)
        delete_button = self.driver.find_element(*self.DELETE_USER_BUTTON)
        delete_button.click()
        confirm_delete = self.driver.find_element(*self.CONFIRM_DELETE_USER_BUTTON)
        confirm_delete.click()

    @allure.step("Проверка отображения окна подтверждения удаления пользователя")
    def assert_confirm_delete_user_is_opened(self):
        self.assert_element_visible(self.CONFIRM_DELETE_USER_BUTTON)
        self.assert_element_visible(self.CANCEL_DELETE_USER_BUTTON)
        self.assert_element_visible(self.DELETE_CONFIRMATION_TITLE)

    @allure.step("Найти кнопку удаления пользователя по номеру")
    def get_delete_user_button(self, user_number):
        return (By.CSS_SELECTOR, f'[data-qa="delete-user-button-{user_number}"]')







