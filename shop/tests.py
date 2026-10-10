from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import CartItem, CustomerProfile, Order, Product, SellerProfile, Store

User = get_user_model()


class RoleIsolationTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(phone="09120000001", password="AdminPass-2026!")
        self.seller_a = User.objects.create_user(phone="09120000002", password="SellerPass-2026!")
        self.seller_b = User.objects.create_user(phone="09120000003", password="SellerPass-2026!")
        profile_a = SellerProfile.objects.create(user=self.seller_a)
        profile_b = SellerProfile.objects.create(user=self.seller_b)
        self.store_a = Store.objects.create(seller=profile_a, name="فروشگاه الف", description="فروشگاه اول")
        self.store_b = Store.objects.create(seller=profile_b, name="فروشگاه ب", description="فروشگاه دوم")
        self.product_a = Product.objects.create(store=self.store_a, name="product-a", price=Decimal("100"), image="products/a.jpg")
        self.product_b = Product.objects.create(store=self.store_b, name="product-b", price=Decimal("200"), image="products/b.jpg")

    def test_each_seller_only_sees_and_edits_own_products(self):
        self.client.force_login(self.seller_a)
        response = self.client.get(reverse("seller_panel"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "product-a")
        self.assertNotContains(response, "product-b")
        self.assertEqual(self.client.get(reverse("seller_edit_product", args=[self.product_b.pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse("seller_edit_product", args=[self.product_a.pk])).status_code, 200)

    def test_admin_sees_products_from_all_stores(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("manager_panel"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "product-a")
        self.assertContains(response, "product-b")


class CustomerShoppingTests(TestCase):
    def setUp(self):
        seller = User.objects.create_user(phone="09120000004", password="SellerPass-2026!")
        seller_profile = SellerProfile.objects.create(user=seller)
        store = Store.objects.create(seller=seller_profile, name="فروشگاه تست", description="تست")
        self.product = Product.objects.create(store=store, name="sample-item", price=Decimal("25"), image="products/sample.jpg")
        self.customer_user = User.objects.create_user(phone="09120000005", password="CustomerPass-2026!")
        self.customer = CustomerProfile.objects.create(user=self.customer_user, phone="09120000000", balance=Decimal("40"))

    def test_customer_adds_to_cart_and_checks_out(self):
        self.client.force_login(self.customer_user)
        response = self.client.post(reverse("add_to_cart", args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CartItem.objects.filter(customer=self.customer, product=self.product).count(), 1)

        response = self.client.post(reverse("checkout"))
        self.assertRedirects(response, reverse("order_history"))
        self.assertEqual(Order.objects.filter(customer=self.customer, is_paid=True).count(), 1)
        self.assertEqual(CartItem.objects.filter(customer=self.customer).count(), 0)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.balance, Decimal("15"))

    def test_public_signup_creates_a_separate_seller_profile(self):
        response = self.client.post(reverse("signup"), {
            "phone": "09120000006",
            "first_name": "Seller",
            "last_name": "Test",
            "password1": "UniqueSellerPass-72!",
            "password2": "UniqueSellerPass-72!",
            "role": "seller",
            "phone": "",
        })
        self.assertRedirects(response, reverse("seller_panel"))
        self.assertTrue(SellerProfile.objects.filter(user__phone="09120000006").exists())
