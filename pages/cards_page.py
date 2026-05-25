import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from pages.base_page import BasePage


class CardsPage(BasePage):
    LOAD_BUTTON = (By.CSS_SELECTOR, 'button.trigger-btn')
    CARDS_ITEMS = (By.CSS_SELECTOR, '.case-element')

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.url = "/automation-lab/cards"

        super().__init__(driver, self.url)

    @allure.step("Загрузка карточек на странице")
    def load_cards(self):
        self.open()
        self.click(self.LOAD_BUTTON)

    @allure.step("Получить список всех карточек")
    def get_all_cards(self):
        return self.driver.find_elements(*self.CARDS_ITEMS)

    @allure.step("Получить количество карточек")
    def get_cards_count(self):
        cards = self.get_all_cards()
        return len(cards)
