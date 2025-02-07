from playwright.sync_api import Page, expect


class ProductPage:

    product_desc_list = []

    def __init__(self, page: Page):
        self.page = page
        # Backpack
        self.addBackpack = "#add-to-cart-sauce-labs-backpack"

        # Bike Light
        self.addBikeLight = "#add-to-cart-sauce-labs-bike-light"
        # Bolt T Shirt
        self.addBoltTShirt = "#add-to-cart-sauce-labs-bolt-t-shirt"
        # Fleece Jacket
        self.addFleeceJacket = "#add-to-cart-sauce-labs-fleece-jacket"
        # Onesie
        self.addOnesie = "#add-to-cart-sauce-labs-onesie"
        # Test.allTheThings() T-Shirt (Red)
        self.addAllTheThingTShirt = (
            "#add-to-cart-test\\.allthethings\\(\\)-t-shirt-\\(red\\)"
        )

        self.product_on_cart_list = []
        self.product_desc_list = []
        ProductPage.product_desc_list = self.product_desc_list

        self.shoppingCartBadge = '[data-test="shopping-cart-badge"]'
        self.shoppingCart = ".shopping_cart_link"

        self.checkoutButton = "#checkout"

    def add_to_cart(self, product):
        if product == "backpack":
            self.page.click(self.addBackpack)
            collect_product = {
                "product": self.page.locator('[data-test="inventory-item-name"]')
                .nth(0)
                .inner_text(),
                "price": float(
                    self.page.locator('[data-test="inventory-item-price"]')
                    .nth(0)
                    .inner_text()
                    .replace("$", "")
                ),
            }
        elif product == "bikeLight":
            self.page.click(self.addBikeLight)
            collect_product = {
                "product": self.page.locator('[data-test="inventory-item-name"]')
                .nth(1)
                .inner_text(),
                "price": float(
                    self.page.locator('[data-test="inventory-item-price"]')
                    .nth(1)
                    .inner_text()
                    .replace("$", "")
                ),
            }
        elif product == "boltTShirt":
            self.page.click(self.addBoltTShirt)
            collect_product = {
                "product": self.page.locator('[data-test="inventory-item-name"]')
                .nth(2)
                .inner_text(),
                "price": float(
                    self.page.locator('[data-test="inventory-item-price"]')
                    .nth(2)
                    .inner_text()
                    .replace("$", "")
                ),
            }
        elif product == "fleeceJacket":
            self.page.click(self.addFleeceJacket)
            collect_product = {
                "product": self.page.locator('[data-test="inventory-item-name"]')
                .nth(3)
                .inner_text(),
                "price": float(
                    self.page.locator('[data-test="inventory-item-price"]')
                    .nth(3)
                    .inner_text()
                    .replace("$", "")
                ),
            }
        elif product == "onesie":
            self.page.click(self.addOnesie)
            collect_product = {
                "product": self.page.locator('[data-test="inventory-item-name"]')
                .nth(4)
                .inner_text(),
                "price": float(
                    self.page.locator('[data-test="inventory-item-price"]')
                    .nth(4)
                    .inner_text()
                    .replace("$", "")
                ),
            }
        elif product == "allTheThingsTShirt":
            self.page.click(self.addAllTheThingTShirt)
            collect_product = {
                "product": self.page.locator('[data-test="inventory-item-name"]')
                .nth(5)
                .inner_text(),
                "price": float(
                    self.page.locator('[data-test="inventory-item-price"]')
                    .nth(5)
                    .inner_text()
                    .replace("$", "")
                ),
            }
        else:
            raise ValueError(f"Product '{product}' is not available.")

        self.product_desc_list.append(collect_product)

    def checkout(self):
        total_product = len(self.product_desc_list)
        assert (
            int(self.page.locator(self.shoppingCartBadge).inner_text()) == total_product
        ), "Total product doesn't match!"
        self.page.locator(self.shoppingCart).click()
        title = self.page.locator(".title")
        assert title.inner_text() == "Your Cart", "Open cart is success but wrong page"
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
            else:
                assert (
                    self.product_desc_list[y] == self.product_on_cart_list[y]
                ), f"Item: {self.product_desc_list[y]}, doesn't matched with item: {self.product_on_cart_list[y]}"
        self.page.click(self.checkoutButton)
        assert (
            title.inner_text() == "Checkout: Your Information"
        ), "Open 'Your Information' page not success!"
