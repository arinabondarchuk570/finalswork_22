import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from pages.base_page import BasePage


class Categories(BasePage):
    CARD_SELECTOR = (By.CSS_SELECTOR, '.feature-card')
    OPEN_BUTTON = (By.XPATH, ".//a[contains(text(), 'Открыть')]")

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.url = ""
        super().__init__(driver, self.url)

    @allure.step("Получить все категории")
    def get_all_categories(self):
        cards = self.driver.find_elements(*self.CARD_SELECTOR)
        return [card.text for card in cards]

    @allure.step("Открыть категорию по имени")
    def open_category_by_name(self, category_name):
        cards = self.driver.find_elements(*self.CARD_SELECTOR)

        for card in cards:
            card_text = card.text
            if category_name.lower() in card_text.lower():
                open_button = card.find_element(*self.OPEN_BUTTON)
                open_button.click()
                time.sleep(1)
                return

    @allure.step("Получить количество категорий")
    def get_categories_count(self):
        cards = self.driver.find_elements(*self.CARD_SELECTOR)
        return len(cards)

    @allure.step("Проверить, что категория существует")
    def assert_category_exists(self, category_name: str):
        categories = self.get_all_categories()
        found = any(category_name.lower() in cat.lower() for cat in categories)
        assert found
