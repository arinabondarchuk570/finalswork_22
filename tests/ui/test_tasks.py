import time

import allure
import pytest
from pages.login_page import LoginPage
from pages.tasks_page import TasksPage
from test_data.users import ADMIN

@allure.feature("Отображение страницы")
@allure.title("Проверка отображения страницы Tasks")
def test_tasks_page_display(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    tasks_page = TasksPage(driver)
    tasks_page.open()
    tasks_page.assert_tasks_page_opened()

@allure.title("Проверка наличия задач у пользователя")
def test_user_has_tasks(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    tasks_page = TasksPage(driver)
    tasks_page.open()
    time.sleep(0.5)
    tasks_count = tasks_page.get_number_of_tasks()
    assert tasks_count > 0
    print(f"У пользователя найдено заданий: {tasks_count}")

@allure.title("Проверка отсутствия задач у пользователя")
@pytest.mark.xfail
def test_user_has_no_tasks(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    tasks_page = TasksPage(driver)
    tasks_page.open()
    tasks_count = tasks_page.get_number_of_tasks()
    assert tasks_count == 0, \
        f"Найдено заданий: {tasks_count}"
    print(f"У пользователя нет заданий")

@allure.feature("Фильтрация задач")
@allure.title("Проверка корректной фильтрации задач по статусу")
@pytest.mark.parametrize("filter_type, badge_type", [
    ("todo", "todo"),
    ("in_progress", "in_progress"),
    ("done", "done"),
], ids=[
    "Фильтр 'к работе'",
    "Фильтр 'в процессе'",
    "Фильтр 'готово'",
])
def test_filter_tasks_by_status(driver, filter_type, badge_type):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    tasks_page = TasksPage(driver)
    tasks_page.open()
    tasks_page.filter_tasks_by_status(filter_type)
    task_rows = driver.find_elements(*tasks_page.TASKS_ROW)
    tasks_count = len(task_rows)
    badges_count = tasks_page.get_number_of_badges(badge_type)
    assert tasks_count == badges_count

@allure.feature("Фильтрация задач")
@allure.title("Проверка корректной фильтрации задач по приоритету")
@pytest.mark.parametrize("filter_type, badge_type", [
    ("high", "high"),
    ("medium", "medium"),
    ("low", "low"),
], ids=[
    "Фильтрация по высокому приоритету",
    "Фильтрация по среднему приоритету",
    "Фильтрация по низкому приоритету",
])
def test_filter_tasks_by_priority(driver, filter_type, badge_type):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    tasks_page = TasksPage(driver)
    tasks_page.open()
    tasks_page.filter_tasks_by_priority(filter_type)
    task_rows = driver.find_elements(*tasks_page.TASKS_ROW)
    tasks_count = len(task_rows)
    badges_count = tasks_page.get_number_of_badges(badge_type)
    assert tasks_count == badges_count

@allure.feature("Поиск задач")
@allure.title("Поиск задач по названию")
@pytest.mark.parametrize("search_text, expected_results", [
    ("настроить ci/cd pipeline", ["Настроить CI/CD pipeline"]),
    ("баги", ["Исправить баги"]),
    ("ОПТИМИЗИРОВАТЬ", ["Оптимизировать запросы к БД"]),
])
def test_search_for_tasks(driver, search_text, expected_results):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    tasks_page = TasksPage(driver)
    tasks_page.open()
    search_results = tasks_page.search_tasks_by_name(search_text)
    assert search_results == expected_results

@allure.feature("Поиск задач")
@allure.title("Негативная проверка поиска задач")
@pytest.mark.parametrize("search_text", [
    "Задача которой не существует",
    "  ",
])
def test_search_tasks_negative(driver, search_text):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    tasks_page = TasksPage(driver)
    tasks_page.open()
    tasks_page.search_tasks_by_name(search_text)
    tasks_page.assert_element_visible(tasks_page.NO_TASKS_FOUND)

@allure.feature("Поиск задач")
@allure.title('Проверка поиска задач с фильтром по статусу')
@pytest.mark.parametrize("search_text, status_type, expected_results", [
    ("обновить дизайн", "todo", ["Обновить дизайн"]),
    ("Оптимизировать запросы ", "in_progress", ["Оптимизировать запросы к БД"]),
    ("добавить логирование", "done", ["Добавить логирование"]),
])
def test_search_boards_with_public_toggle(driver, search_text, status_type, expected_results):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(ADMIN)

    tasks_page = TasksPage(driver)
    tasks_page.open()
    tasks_page.filter_tasks_by_status(status_type)
    search_results = tasks_page.search_tasks_by_name(search_text)
    task_rows = driver.find_elements(*tasks_page.TASKS_ROW)
    tasks_count = len(task_rows)
    status_count = tasks_page.get_number_of_badges(status_type)
    assert search_results == expected_results
    assert tasks_count == status_count
