import time

import allure
import pytest
from pages.boards_page import BoardsPage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.tasks_page import TasksPage
from test_data.users import ADMIN, CHARLI

@allure.feature("Отображение страницы")
@allure.title("Тест открыта ли страница Dashboard")
def test_dashboard_page_display(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(CHARLI)

    dashboard_page = DashboardPage(driver)
    dashboard_page.open()
    dashboard_page.assert_that_dashboard_opened()

@allure.feature("Синхронизация")
@pytest.mark.xfail(reason="Страница Dashboard отображает на одну доску меньше чем на самом деле есть в Boards")
@allure.title("Проверка синхронизации страниц Dashboard и Boards")
def test_boards_count_difference_between_pages(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.wait_page_opened()
    login_page.login(ADMIN)

    dashboard = DashboardPage(driver)
    dashboard.open()
    dashboard.wait_page_opened()
    dashboard_count_boards = dashboard.get_boards_number()

    boards = BoardsPage(driver)
    boards.open()
    boards.wait_page_opened()
    boards_count = boards.get_number_of_boards()

    assert dashboard_count_boards == boards_count, f"На Dashboard {dashboard_count_boards}, на Boards {boards_count}"

@allure.feature("Синхронизация")
@allure.title("Проверка синхронизации страниц Dashboard и Tasks")
def test_tasks_count_difference_between_pages(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    dashboard = DashboardPage(driver)
    dashboard.open()
    dashboard_count_tasks = dashboard.get_tasks_number()

    tasks = TasksPage(driver)
    tasks.open()
    tasks_count = tasks.get_number_of_tasks()

    assert dashboard_count_tasks == tasks_count, f"На Dashboard {dashboard_count_tasks}, на Tasks {tasks_count}"

@allure.feature("Синхронизация")
@allure.title("Проверка синхронизации задач в процессе на страницах Dashboard и Tasks")
def test_in_progress_count_dif(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    dashboard = DashboardPage(driver)
    dashboard.open()
    dashboard_count_in_progress = dashboard.get_in_progress_number()

    tasks = TasksPage(driver)
    tasks.open()
    tasks.filter_tasks_by_status("in_progress")
    time.sleep(0.5)
    tasks_count_in_progress = tasks.get_number_of_tasks()

    assert dashboard_count_in_progress == tasks_count_in_progress, \
        f"На Dashboard {dashboard_count_in_progress}, на Tasks {tasks_count_in_progress}"

@allure.feature("Синхронизация")
@allure.title("Проверка синхронизации завершённых задач на страницах Dashboard и Tasks")
def test_done_count_dif(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    dashboard = DashboardPage(driver)
    dashboard.open()
    dashboard_count_done = dashboard.get_done_number()

    tasks = TasksPage(driver)
    tasks.open()
    tasks.filter_tasks_by_status("done")
    time.sleep(0.5)
    tasks_count_done = tasks.get_number_of_tasks()

    assert dashboard_count_done == tasks_count_done, \
        f"На Dashboard {dashboard_count_done}, на Tasks {tasks_count_done}"

@allure.title("Проверка корректного перехода на страницы с Dashboard")
@pytest.mark.parametrize("method_name, expected_url", [
    ("go_to_homepage", "/dashboard"),
    ("go_to_all_boards", "/boards"),
    ("go_to_all_tasks", "/tasks"),
])
def test_dashboard_page_navigation(driver, method_name, expected_url):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    dashboard = DashboardPage(driver)
    dashboard.open()

    use_method = getattr(dashboard, method_name)
    use_method()

    assert expected_url in driver.current_url

@allure.title("Проверка корректного выхода из профиля")
def test_logout(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(CHARLI)

    dashboard = DashboardPage(driver)
    dashboard.open()
    dashboard.logout()

    expected_url = "/login"
    assert expected_url in driver.current_url
