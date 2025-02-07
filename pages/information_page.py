from playwright.sync_api import Page, expect


class InformationPage:
    def __init__(self, page: Page):
        self.page = page
        self.firstName_input = "#first-name"
        self.lastName_input = "#last-name"
        self.postalCode_input = "#postal-code"

        self.continue_button = "#continue"

    def fill_information(self, information):
        list_information = list(information)
        self.page.locator(self.firstName_input).fill(list_information[0])
        self.page.locator(self.lastName_input).fill(list_information[1])
        self.page.locator(self.postalCode_input).fill(list_information[2])

    def click_continue(self):
        self.page.click(self.continue_button)
        title = self.page.locator(".title")
        assert (
            title.inner_text() == "Checkout: Overview"
        ), "Continue success but wrong page"
