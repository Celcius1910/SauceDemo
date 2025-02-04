import pytest
from pages.login_page import *

def test_valid_login(page):
    login_page = LoginPage(page)
    login_page.load()
    login_page.login("standard_user", "secret_sauce")
    assert login_page.is_logged_in()
