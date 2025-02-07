from playwright.sync_api import Page, expect
from pages.product_page import ProductPage


class OverviewPage:
    def __init__(self, page: Page):
        self.page = page
        self.product_desc_list = ProductPage.product_desc_list
        self.product_on_cart_list = []
        self.subtotal = '[data-test="subtotal-label"]'
        self.tax = '[data-test="tax-label"]'
        self.total = '[data-test="total-label"]'
        self.total_price_list = []
        self.finish_button = "#finish"
        self.completeOrder = ".complete-header"

    def calculate_tax_percentage(subtotal, tax_amount):
        return (tax_amount / subtotal) * 100

    def calculate_total(subtotal, tax_percentage):
        tax_amount = (tax_percentage / 100) * subtotal
        return round(subtotal + tax_amount, 2)

    def validate_cart(self, product):
        total_product = len(self.product_desc_list)
        for y in range(total_product):
            if y == 0:
                for i in range(total_product):
                    collect_product = {
                        "product": self.page.locator(
                            '[data-test="inventory-item-name"]'
                        )
                        .nth(i)
                        .inner_text(),
                        "price": float(
                            self.page.locator('[data-test="inventory-item-price"]')
                            .nth(i)
                            .inner_text()
                            .replace("$", "")
                        ),
                    }
                    self.product_on_cart_list.append(collect_product)
                    self.total_price_list.append(collect_product["price"])
            else:
                assert (
                    self.product_desc_list[y] == self.product_on_cart_list[y]
                ), f"Item: {self.product_desc_list[y]}, doesn't matched with item: {self.product_on_cart_list[y]}"

        total_price = sum(self.total_price_list)
        assert (
            float(
                self.page.locator(self.subtotal)
                .inner_text()
                .replace("Item total: $", "")
            )
            == total_price
        ), "Wrong subtotal"
        tax_amount = float(
            self.page.locator(self.tax).inner_text().replace("Tax: $", "")
        )
        calculated_tax_percentage = OverviewPage.calculate_tax_percentage(
            total_price, tax_amount
        )
        calculated_total = OverviewPage.calculate_total(
            total_price, calculated_tax_percentage
        )
        assert (
            float(self.page.locator(self.total).inner_text().replace("Total: $", ""))
            == calculated_total
        ), "Wrong total"

    def click_finish(self):
        self.page.click(self.finish_button)
        expect(self.page.locator(self.completeOrder)).to_be_visible()
