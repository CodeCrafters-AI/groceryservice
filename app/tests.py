from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Product, Order, Cart, Payment
from decimal import Decimal

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            phone_number="1234567890",
            address="123 Test St",
            preferred_payment_method="Credit Card",
            is_customer=True
        )

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.phone_number, "1234567890")
        self.assertEqual(self.user.preferred_payment_method, "Credit Card")

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="A test product",
            price=Decimal("10.00"),
            stock=100,
            category="Electronics"
        )

    def test_product_creation(self):
        self.assertTrue(isinstance(self.product, Product))
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, Decimal("10.00"))
        self.assertEqual(self.product.stock, 100)

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.product = Product.objects.create(name="Test Product", price=Decimal("10.00"), stock=100, category="Electronics")
        self.order = Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=2,
            total_price=Decimal("20.00"),
            status="Pending"
        )

    def test_order_creation(self):
        self.assertTrue(isinstance(self.order, Order))
        self.assertEqual(self.order.user.username, "testuser")
        self.assertEqual(self.order.product.name, "Test Product")
        self.assertEqual(self.order.quantity, 2)
        self.assertEqual(self.order.total_price, Decimal("20.00"))

class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.product = Product.objects.create(name="Test Product", price=Decimal("10.00"), stock=100, category="Electronics")
        self.cart_item = Cart.objects.create(
            user=self.user,
            product=self.product,
            quantity=3
        )

    def test_cart_item_creation(self):
        self.assertTrue(isinstance(self.cart_item, Cart))
        self.assertEqual(self.cart_item.user.username, "testuser")
        self.assertEqual(self.cart_item.product.name, "Test Product")
        self.assertEqual(self.cart_item.quantity, 3)

    def test_cart_item_total_price(self):
        self.assertEqual(self.cart_item.get_total_price(), Decimal("30.00"))

class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.product = Product.objects.create(name="Test Product", price=Decimal("10.00"), stock=100, category="Electronics")
        self.order = Order.objects.create(user=self.user, product=self.product, quantity=2, total_price=Decimal("20.00"))
        self.payment = Payment.objects.create(
            order=self.order,
            amount=self.order.total_price,
            payment_method="Credit Card",
            payment_status="Pending"
        )

    def test_payment_creation(self):
        self.assertTrue(isinstance(self.payment, Payment))
        self.assertEqual(self.payment.order, self.order)
        self.assertEqual(self.payment.amount, Decimal("20.00"))
        self.assertEqual(self.payment.payment_method, "Credit Card")
        self.assertEqual(self.payment.payment_status, "Pending")
