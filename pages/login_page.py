from playwright.sync_api import Page
from utils.config import *


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = "#user-name"
        self.password_input = "#password"
        self.login_button = "#login-button"
        self.error_message = "[data-test='error']"

    def load(self):
        self.page.goto(BASE_URL)

    def login(self, username, password):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)

    def is_logged_in(self):
        title = self.page.locator(".title")
        assert title.inner_text() == "Products", "Login success but wrong page"
        return self.page.is_visible(".title")

    def get_error_message(self):
        return self.page.inner_text(self.error_message)
