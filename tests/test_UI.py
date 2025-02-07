import pytest
from pages import LoginPage, ProductPage, InformationPage, OverviewPage
import allure


@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.parametrize(
    "credentials, expected_error",
    [
        ({"username": "standard_user", "password": "secret_sauce"}, None),
        ({"username": "locked_out_user", "password": "secret_sauce"}, "Epic sadface"),
        ({"username": "problem_user", "password": "secret_sauce"}, None),
        ({"username": "performance_glitch_user", "password": "secret_sauce"}, None),
        ({"username": "error_user", "password": "secret_sauce"}, None),
        ({"username": "visual_user", "password": "secret_sauce"}, None),
    ],
)
def test_valid_login(page, credentials, expected_error):
    login_page = LoginPage(page)
    login_page.load()
    login_page.login(credentials["username"], credentials["password"])

    if expected_error:
        error_message = login_page.get_error_message()
        assert (
            expected_error in error_message
        ), f"Expected '{expected_error}', but got '{error_message}'"
    else:
        assert login_page.is_logged_in()


@pytest.mark.parametrize(
    "product, information",
    [
        (
            (
                "backpack",
                "bikeLight",
                "boltTShirt",
                "fleeceJacket",
                "onesie",
                "allTheThingsTShirt",
            ),
            ("John", "Doe", "12345"),
        ),
        (
            ("backpack", "bikeLight", "boltTShirt", "fleeceJacket", "onesie"),
            ("Naufal", "Aziz", "17520"),
        ),
    ],
)
def test_add_to_cart(page, product, information):
    login_page = LoginPage(page)
    login_page.load()
    login_page.login("standard_user", "secret_sauce")
    product_page = ProductPage(page)
    list_product = list(product)
    total_product = len(list_product)
    for i in range(total_product):
        product_page.add_to_cart(product[i])
    product_page.checkout()
    information_page = InformationPage(page)
    information_page.fill_information(information)
    information_page.click_continue()
    overview_page = OverviewPage(page)
    overview_page.validate_cart(product)
    overview_page.click_finish()
