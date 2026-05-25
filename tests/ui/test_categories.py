import allure
from pages.categories_page import Categories
from pages.login_page import LoginPage
from test_data.users import ADMIN
from config import BaseConfig

@allure.feature("Навигация")
@allure.title("Открытие категории 'Карточки данных'")
def test_open_data_cards_category(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    categories_page = Categories(driver)
    categories_page.open()
    categories_page.open_category_by_name("Карточки данных")

    assert BaseConfig.ROOT_PATH + "/automation-lab/cards" in driver.current_url


@allure.feature("Навигация")
@allure.title("Открытие категории 'Форма подписки'")
def test_open_data_subscription_category(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    categories_page = Categories(driver)
    categories_page.open()
    categories_page.open_category_by_name("Форма подписки")

    assert BaseConfig.ROOT_PATH + "/automation-lab/subscription" in driver.current_url


@allure.feature("Навигация")
@allure.title("Открытие категории 'Система управления задачами'")
def test_open_task_category(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    categories_page = Categories(driver)
    categories_page.open()
    categories_page.open_category_by_name("Система управления задачами")

    assert BaseConfig.ROOT_PATH + "/dashboard" in driver.current_url
