import re

import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class BoardsPage(BasePage):
    #Локаторы кнопок
    CREATE_BOARD_BUTTON = (By.CSS_SELECTOR, '[class="btn btn-primary btn-md"]')
    CHECKBOX_PUBLIC_ONLY = (By.CSS_SELECTOR, '[data-qa="boards-public-only-checkbox"]')
    #Локаторы связанные с поиском
    BOARDS_SEARCH_INPUT = (By.CSS_SELECTOR, '[data-qa="boards-search-input"]')
    NO_BOARDS_FOUND = (By.CSS_SELECTOR, '.admin-table-empty')
    #Локаторы заголовков
    BOARDS_H1 = (By.CSS_SELECTOR, '[data-qa="boards-page-title"]')
    #Локаторы таблицы досок
    BOARDS_ROWS = (By.XPATH, "//tbody/tr")
    PUBLIC_YES = (By.XPATH, "//span[contains(@class, 'admin-role-badge') and text()='Да']")
    PUBLIC_NO = (By.XPATH, "//span[contains(@class, 'admin-role-badge') and text()='Нет']")
    BOARD_NAMES = (By.CSS_SELECTOR, 'td:first-child')
    BOARDS_COUNTER = (By.CSS_SELECTOR, '.admin-section-title')
    #Локаторы создания доски
    CREATE_BOARD_TITLE_INPUT = (By.CSS_SELECTOR, '[data-qa="create-board-title-input"]')
    CREATE_BOARD_DESCRIPTION_INPUT = (By.CSS_SELECTOR, '[data-qa="create-board-description-textarea"]')
    CREATE_BOARD_PUBLIC_CHECKBOX = (By.CSS_SELECTOR, '[data-qa="create-board-public-checkbox"]')
    SUBMIT_NEW_BOARD = (By.CSS_SELECTOR, '[data-qa="create-board-submit-button"]')
    CANCEL_NEW_BOARD = (By.CSS_SELECTOR, '[data-qa="create-board-cancel-button"]')
    BOARD_CREATED = (By.CSS_SELECTOR, ".toast-message")

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.url = "/boards"

        super().__init__(driver, self.url)

    @allure.step("Получить количество досок")
    def get_number_of_boards(self):
        count_boards_element = self.driver.find_element(*self.BOARDS_COUNTER)
        boards_number_text = count_boards_element.text

        match = re.search(r'\((\d+)\)', boards_number_text)
        if match:
            return int(match.group(1))
        numbers = re.findall(r'\d+', boards_number_text)
        if numbers:
            return int(numbers[0])

    @allure.step("Проверка загрузки страницы boards")
    def assert_boards_page_opened(self):
        self.assert_element_visible(self.BOARDS_SEARCH_INPUT)
        self.assert_element_visible(self.BOARDS_H1)
        self.assert_element_visible(self.CREATE_BOARD_BUTTON)

    @allure.step("Поиск досок по имени")
    def search_boards_by_name(self, search_text):
        search_input = self.driver.find_element(*self.BOARDS_SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(search_text)
        board_name_elements = [board.text for board in self.driver.find_elements(*self.BOARD_NAMES)]
        return board_name_elements

    @allure.step("Просматривать только публичные доски")
    def filter_public_boards_only(self):
        self.driver.find_element(*self.CHECKBOX_PUBLIC_ONLY).click()

    @allure.step("Проверка что доска публичная")
    def assert_board_is_public(self):
        self.assert_element_visible(self.PUBLIC_YES)

    @allure.step("Проверка что доска приватная")
    def assert_board_not_public(self):
        self.assert_element_visible(self.PUBLIC_NO)

    @allure.step("Проверка отображения окна создания доски")
    def assert_create_board_opened(self):
        self.assert_element_visible(self.CREATE_BOARD_TITLE_INPUT)
        self.assert_element_visible(self.CREATE_BOARD_DESCRIPTION_INPUT)
        self.assert_element_visible(self.SUBMIT_NEW_BOARD)
        self.assert_element_visible(self.CANCEL_NEW_BOARD)

    @allure.step("Создание доски")
    def create_board(self, title_text, description_text, is_public = False):
        self.driver.find_element(*self.CREATE_BOARD_BUTTON).click()
        title_input = self.driver.find_element(*self.CREATE_BOARD_TITLE_INPUT)
        title_input.click()
        title_input.send_keys(title_text)
        description_input = self.driver.find_element(*self.CREATE_BOARD_DESCRIPTION_INPUT)
        description_input.click()
        description_input.send_keys(description_text)

        if is_public:
            self.driver.find_element(*self.CREATE_BOARD_PUBLIC_CHECKBOX).click()

        self.click(self.SUBMIT_NEW_BOARD)




