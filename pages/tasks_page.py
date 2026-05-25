import re

import allure
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class TasksPage(BasePage):
    #Локаторы поиска
    SEARCH_TASKS = (By.ID, 'id-input-tasks-search-input')
    NO_TASKS_FOUND = (By.CSS_SELECTOR, '.admin-table-empty')
    #Локаторы статуса
    STATUS_FILTER = (By.CSS_SELECTOR, '[data-qa="tasks-status-filter"]')
    OPTION_TODO_FILTER = (By.CSS_SELECTOR, '[data-qa="tasks-status-filter"] option[value="todo"]')
    OPTION_IN_PROGRESS_FILTER = (By.CSS_SELECTOR, '[data-qa="tasks-status-filter"] option[value="in_progress"]')
    OPTION_ALL_FILTER = (By.CSS_SELECTOR, '[data-qa="tasks-status-filter"] option[value=""]')
    OPTION_DONE_FILTER = (By.CSS_SELECTOR, '[data-qa="tasks-status-filter"] option[value="done"]')
    #Локаторы приоритета
    PRIORITY_FILTER = (By.CSS_SELECTOR, '[data-qa="tasks-priority-filter"]')
    OPTION_PRIORITY_ALL = (By.CSS_SELECTOR, '[data-qa="tasks-priority-filter"] option[value=""]')
    OPTION_PRIORITY_LOW = (By.CSS_SELECTOR, '[data-qa="tasks-priority-filter"] option[value="low"]')
    OPTION_PRIORITY_MEDIUM = (By.CSS_SELECTOR, '[data-qa="tasks-priority-filter"] option[value="medium"]')
    OPTION_PRIORITY_HIGH = (By.CSS_SELECTOR, '[data-qa="tasks-priority-filter"] option[value="high"]')
    #Локаторы бейджей
    TODO_BADGE = (By.XPATH, "//span[contains(@class, 'admin-role-badge') and text()='В работу']")
    IN_PROGRESS_BADGE = (By.XPATH, "//span[contains(@class, 'admin-role-badge') and text()='В работе']")
    DONE_BADGE = (By.XPATH, "//span[contains(@class, 'admin-role-badge') and text()='Выполнено']")
    PRIORITY_LOW_BADGE = (By.CSS_SELECTOR, '.admin-role-badge--priority-low')
    PRIORITY_MEDIUM_BADGE = (By.CSS_SELECTOR, '.admin-role-badge--priority-medium')
    PRIORITY_HIGH_BADGE = (By.CSS_SELECTOR, '.admin-role-badge--priority-high')
    #Локаторы таблицы
    TASKS_BAR = (By.CSS_SELECTOR, '[class="admin-table-container"]')
    TASKS_ROW = (By.XPATH, "//tbody/tr")
    TASKS_COUNTER = (By.CSS_SELECTOR, '.admin-section-title')
    ALL_TASKS_NAMES = (By.CSS_SELECTOR, 'td:first-child')

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.url = '/tasks'

        super().__init__(driver, self.url)

    @allure.step("Проверка загрузки страницы tasks")
    def assert_tasks_page_opened(self):
        self.assert_element_visible(self.SEARCH_TASKS)
        self.assert_element_visible(self.STATUS_FILTER)
        self.assert_element_visible(self.PRIORITY_FILTER)

    @allure.step("Фильтровать задачи по статусу")
    def filter_tasks_by_status(self, status):
        statuses_available = {
            'todo': self.OPTION_TODO_FILTER,
            'in_progress': self.OPTION_IN_PROGRESS_FILTER,
            'done': self.OPTION_DONE_FILTER,
            'all': self.OPTION_ALL_FILTER
        }
        self.click(self.STATUS_FILTER)
        self.click(statuses_available[status])

    @allure.step("Фильтровать задачи по приоритету")
    def filter_tasks_by_priority(self, priority):
        priorities_available = {
            'all': self.OPTION_PRIORITY_ALL,
            'low': self.OPTION_PRIORITY_LOW,
            'medium': self.OPTION_PRIORITY_MEDIUM,
            'high': self.OPTION_PRIORITY_HIGH
        }
        self.click(self.PRIORITY_FILTER)
        self.click(priorities_available[priority])

    @allure.step("Искать задачи по тексту")
    def search_tasks(self, search_text):
        search_input = self.driver.find_element(*self.SEARCH_TASKS)
        search_input.clear()
        search_input.send_keys(search_text + Keys.ENTER)

    @allure.step("Ожидание загрузки страницы задач")
    def wait_for_tasks_page_to_load(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.TASKS_BAR)
        )

    @allure.step("Получить количество задач")
    def get_number_of_tasks(self):
        count_tasks_element = self.driver.find_element(*self.TASKS_COUNTER)
        tasks_number_text = count_tasks_element.text

        match = re.search(r'\((\d+)\)', tasks_number_text)
        if match:
            return int(match.group(1))
        numbers = re.findall(r'\d+', tasks_number_text)
        if numbers:
            return int(numbers[0])

    @allure.step("Посчитать количество бейджей на странице")
    def get_number_of_badges(self, badge):
        badges_available = {
            'todo': self.TODO_BADGE,
            'in_progress': self.IN_PROGRESS_BADGE,
            'done': self.DONE_BADGE,
            'high': self.PRIORITY_HIGH_BADGE,
            'medium': self.PRIORITY_MEDIUM_BADGE,
            'low': self.PRIORITY_LOW_BADGE
        }
        if badge == "all":
            return self.get_number_of_tasks()
        badge_type = badges_available.get(badge)
        badges = self.driver.find_elements(*badge_type)
        return len(badges)

    @allure.step("Поиск задач по имени")
    def search_tasks_by_name(self, search_text):
        search_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.SEARCH_TASKS)
        )

        search_input.click()
        search_input.clear()
        search_input.send_keys(search_text + Keys.ENTER)

        task_names = [task.text for task in self.driver.find_elements(*self.ALL_TASKS_NAMES)]
        return list(dict.fromkeys(task_names))
