import time
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.webdriver import WebDriver

from config import BaseConfig
from tests.api.api_client import ApiClient


def pytest_addoption(parser):
    parser.addoption("--br", action="store", default="chrome", help="the name of the browser")
    parser.addoption(
        "--allure-print",
        action="store_true",
        default=True,
        help="Включить вывод шагов Allure в консоль.",
    )
    parser.addoption(
        "--locale",
        action="store",
        default="en",
        help="Locale to run tests in (e.g. en, ru).",
    )


@pytest.fixture(scope="session")
def locale(pytestconfig):
    return pytestconfig.getoption("--locale")


@pytest.fixture(autouse=False)
def driver(request, pytestconfig):
    browser = pytestconfig.getoption("--br")
    if browser == "firefox":
        opts = FirefoxOptions()
        opts.add_argument("--width=1980")
        opts.add_argument("--height=1600")
        web_driver = webdriver.Firefox(options=opts)

    else:
        opts = Options()
        opts.add_argument("--incognito")

        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        }
        opts.add_experimental_option("prefs", prefs)

        web_driver = webdriver.Chrome(options=opts)
        web_driver.maximize_window()
        web_driver.implicitly_wait(3)

    yield web_driver
    web_driver.quit()


@pytest.fixture(scope="function")
def api_admin():
    base_url = BaseConfig.ROOT_PATH

    login_url = f"{base_url}{BaseConfig.LOGIN_ENDPOINT}"
    login_data = {
        "email": BaseConfig.ADMIN_EMAIL,
        "password": BaseConfig.ADMIN_PASSWORD
    }
    login_response = requests.post(login_url, json=login_data)
    if login_response.status_code != 200:
        raise Exception(f"Не удалось получить токен")
    token = login_response.json().get("access_token")
    if not token:
        raise Exception("Токен не найден в ответе сервера")
    return ApiClient(base_url, token)


