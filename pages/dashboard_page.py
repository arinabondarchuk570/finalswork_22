import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DashboardPage(BasePage):
    #Локаторы кнопок
    CREATE_BOARD_BUTTON = (By.CSS_SELECTOR, '[data-qa="dashboard-create-board-button"]')
    LOGOUT_BUTTON = (By.CSS_SELECTOR, '[data-qa="header-logout-button"]')
    #Локаторы статистики
    BOARDS_STAT_VALUE = (By.CSS_SELECTOR, '[data-qa="dashboard-stat-total-boards-value"]')
    TASKS_STAT_VALUE = (By.CSS_SELECTOR, '[data-qa="dashboard-stat-total-tasks-value"]')
    IN_PROGRESS_STAT_VALUE = (By.CSS_SELECTOR, '[data-qa="dashboard-stat-in-progress-value"]')
    DONE_STAT_VALUE = (By.CSS_SELECTOR, '[data-qa="dashboard-stat-done-value"]')
    #Локаторы заголовков
    USER_HEADER = (By.CSS_SELECTOR, '[data-qa="header-user-info"]')

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.url = '/dashboard'

        super().__init__(driver, self.url)

    @allure.step("Проверка того, что страница Dashboard открыта")
    def assert_that_dashboard_opened(self):
        self.assert_that_page_opened()
        self.assert_element_visible(self.CREATE_BOARD_BUTTON)

    @allure.step("Создание доски")
    def create_board(self):
        self.click(self.CREATE_BOARD_BUTTON)

    @allure.step("Получить количество досок")
    def get_boards_number(self):
        boards_element = self.driver.find_element(*self.BOARDS_STAT_VALUE)
        boards_text = boards_element.text
        return int(boards_text)

    @allure.step("Получить количество заданий")
    def get_tasks_number(self):
        tasks_element = self.driver.find_element(*self.TASKS_STAT_VALUE)
        tasks_text = tasks_element.text
        return int(tasks_text)

    @allure.step("Получить количество заданий в процессе")
    def get_in_progress_number(self):
        in_progress_element = self.driver.find_element(*self.IN_PROGRESS_STAT_VALUE)
        in_progress_text = in_progress_element.text
        return int(in_progress_text)

    @allure.step("Получить количество выполненных заданий")
    def get_done_number(self):
        done_element = self.driver.find_element(*self.DONE_STAT_VALUE)
        done_text = done_element.text
        return int(done_text)

    @allure.step("Выход из аккаунта")
    def logout(self):
        self.driver.find_element(*self.USER_HEADER).click()
        self.driver.find_element(*self.LOGOUT_BUTTON).click()
