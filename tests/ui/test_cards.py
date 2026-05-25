import allure
from pages.cards_page import CardsPage
from pages.login_page import LoginPage
from test_data.users import ADMIN


@allure.feature("Карточки")
@allure.title("Проверка успешной загрузки карточек")
def test_cards_load_success(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    cards_page = CardsPage(driver)
    cards_page.load_cards()

    cards_count = cards_page.get_cards_count()
    assert cards_count > 0
    print(f"Загружено карточек: {cards_count}")
