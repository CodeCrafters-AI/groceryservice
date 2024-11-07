from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, Cart, Order, Payment

User = get_user_model()

# A. User Management and Authentication

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email,', 'password', 'phone_number', 'is_customer', 'is_delivery_personnel']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
            is_customer=validated_data['is_customer'],
            is_delivery_personnel=validated_data['is_delivery_personnel']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid login credentials")

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'address', 'preferred_payment_method']

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'address', 'preferred_payment_method']

# B. Product Management

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'stock', 'description']

class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'stock', 'description']

class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'stock', 'description']

# C. Cart and Checkout

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity', 'added_at']

class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    products = CartSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'products', 'total_price', 'status', 'created_at', 'delivery_time']

# D. Payment Integration

class PaymentInitiateSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    payment_method = serializers.CharField()

class PaymentVerifySerializer(serializers.Serializer):
    payment_id = serializers.CharField()
    order_id = serializers.IntegerField()
    status = serializers.CharField()

class PaymentHistorySerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'status', 'created_at']

# E. Delivery Management

class AssignDeliveryPartnerSerializer(serializers.Serializer):
    delivery_personnel_id = serializers.IntegerField()

class DeliveryStatusUpdateSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    status = serializers.CharField()
