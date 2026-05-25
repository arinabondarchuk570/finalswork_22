import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from config import BaseConfig
from selenium.webdriver.common.by import By

class BasePage:
    #Локаторы боковой панели
    SIDEBAR_HOME_LINK = (By.CSS_SELECTOR, '[data-qa="sidebar-home-link"]')
    SIDEBAR_ALL_BOARDS = (By.CSS_SELECTOR, '[data-qa="sidebar-boards-link"]')
    SIDEBAR_ALL_TASKS = (By.CSS_SELECTOR, '[data-qa="sidebar-tasks-link"]')
    HEADER_USER_MENU = (By.CSS_SELECTOR, '[data-qa="header-user-menu"]')

    def __init__(self, driver, url, timeout=BaseConfig.WEB_DRIVER_WAIT, title='Task Management Board'):
        self.driver: WebDriver = driver
        self.url = url
        self.title = title

        self.wait = WebDriverWait(driver, timeout)

    @allure.step(f"Открыть страницу")
    def open(self):
        self.driver.get(f"{BaseConfig.ROOT_PATH}{self.url}")

    @allure.step("Ожидание отображения локатора")
    def wait_locator_visible(self, locator):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        return el

    @allure.step(f"Ожидание открытия страницы")
    def wait_page_opened(self):
        self.wait.until(EC.url_contains(self.url))

    @allure.step("Кликнуть на локатор")
    def click(self, locator, is_force=False):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        if is_force:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            self.driver.execute_script("arguments[0].click();", el)
        else:
            el.click()

    @allure.step("Ввести значение в поле")
    def send_keys(self, locator, value):
        el = self.wait_locator_visible(locator)
        el.send_keys(value)

    @allure.step("Проверка видимости элемента")
    def assert_element_visible(self, locator):
        el = self.wait_locator_visible(locator)
        assert el.is_displayed(), f"Элемент '{locator[-1]}' не найден"

    @allure.step("Проверка открыта ли страница")
    def assert_that_page_opened(self):
        self.wait_page_opened()
        assert self.url in self.driver.current_url, f"Expected: {self.url}, but {self.driver.current_url}"
        assert self.title == self.driver.title

    @allure.step("Перейти на главную страницу")
    def go_to_homepage(self):
        self.click(self.SIDEBAR_HOME_LINK)

    @allure.step("Перейти на страницу досок")
    def go_to_all_boards(self):
        self.click(self.SIDEBAR_ALL_BOARDS)

    @allure.step("Перейти на страницу задач")
    def go_to_all_tasks(self):
        self.click(self.SIDEBAR_ALL_TASKS)

    @allure.step("Открыть меню пользователя")
    def open_user_menu(self):
        self.click(self.HEADER_USER_MENU)

