from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Sum, Count
from datetime import timedelta
from django.utils import timezone

from .models import User, Product, Cart, Order, Payment
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
    ProductSerializer,
    AddToCartSerializer,
    CartSerializer,
    OrderSerializer,
    PaymentInitiateSerializer,
    PaymentVerifySerializer,
    PaymentHistorySerializer,
    AssignDeliveryPartnerSerializer,
    DeliveryStatusUpdateSerializer
)

def home_page(request):
    """
    Home page view that displays products to users.
    """
    # Fetch all products to display on the homepage
    products = Product.objects.all()

    # Create context to pass to the template
    context = {
        'products': products
    }

    return render(request, 'index.html', context)


# A. User Management and Authentication

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'User registered successfully',
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # email = serializer.validated_data.get('username')
            # password = serializer.validated_data.get('password')
            email = request.data['username']
            password = request.data['password']
            # Check if the email and password are correct
            print(f"Email: {email}, Password: {password}")

            user = authenticate(request, username=email, password=password)
            print(f"Authenticated user: {user}")  # Debugging line

            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid login credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UpdateProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# B. Product Management

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductSearchView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        if query:
            return Product.objects.filter(name__icontains=query)
        return Product.objects.all()


class AddProductView(APIView):
    #permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProductView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteProductView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)


# C. Cart and Checkout

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, productId):
        cart_item = Cart.objects.filter(user=request.user, product__id=productId).first()
        if cart_item:
            cart_item.delete()
            return Response({'message': 'Item removed from cart'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, orderId):
        order = Order.objects.get(pk=orderId, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


# D. Payment Integration

class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentInitiateSerializer(data=request.data)
        if serializer.is_valid():
            # Assume we integrate payment gateways here
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentVerifySerializer(data=request.data)
        if serializer.is_valid():
            # Handle payment verification logic here
            return Response({'message': 'Payment verified successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(user=request.user)
        serializer = PaymentHistorySerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# E. Delivery Management

class TrackOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, orderId):
        order = Order.objects.get(pk=orderId, user=request.user)
        serializer = OrderSerializer(order)
        return Response({
            'order_id': order.id,
            'delivery_status': order.delivery_status
        }, status=status.HTTP_200_OK)


class AssignDeliveryPartnerView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, orderId):
        serializer = AssignDeliveryPartnerSerializer(data=request.data)
        if serializer.is_valid():
            order = Order.objects.get(pk=orderId)
            order.delivery_personnel_id = serializer.validated_data['delivery_partner_id']
            order.save()
            return Response({'message': 'Delivery partner assigned successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateDeliveryStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DeliveryStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            order = Order.objects.get(pk=serializer.validated_data['order_id'], delivery_personnel=request.user)
            order.delivery_status = serializer.validated_data['status']
            order.save()
            return Response({'message': 'Delivery status updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Combined Analytics View
class CombinedAnalyticsView(APIView):
    def get(self, request):
        # Dashboard Overview Data
        total_users = User.objects.count()
        total_orders = Order.objects.count()
        completed_orders = Order.objects.filter(status='Completed').count()
        pending_orders = Order.objects.filter(status='Pending').count()
        total_revenue = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        total_products = Product.objects.count()
        total_sold = Order.objects.filter(status='Completed').aggregate(Sum('quantity'))['quantity__sum'] or 0

        # Recent Order Analytics (Last Month)
        one_month_ago = timezone.now() - timedelta(days=30)
        recent_orders = Order.objects.filter(created_at__gte=one_month_ago)
        total_recent_orders = recent_orders.count()
        completed_recent_orders = recent_orders.filter(status='Completed').count()
        pending_recent_orders = recent_orders.filter(status='Pending').count()
        recent_revenue = Payment.objects.filter(created_at__gte=one_month_ago).aggregate(Sum('amount'))[
                             'amount__sum'] or 0

        # Product Analytics (Total Sold and Revenue)
        product_stats = []
        products = Product.objects.all()
        for product in products:
            total_sold_for_product = \
            Order.objects.filter(product=product, status='Completed').aggregate(Sum('quantity'))['quantity__sum'] or 0
            revenue_for_product = Payment.objects.filter(order__product=product).aggregate(Sum('amount'))[
                                      'amount__sum'] or 0
            product_stats.append({
                'product_name': product.name,
                'total_sold': total_sold_for_product,
                'revenue': revenue_for_product
            })

        # Revenue Over Time (Last 30 Days)
        recent_dates = [(timezone.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]
        recent_revenue_data = [
            Payment.objects.filter(created_at__date=date).aggregate(Sum('amount'))['amount__sum'] or 0 for date in
            recent_dates]

        # Payment Methods Distribution
        payment_methods = Payment.objects.values('payment_method').annotate(method_count=Count('id'))
        payment_methods_labels = [p['payment_method'] for p in payment_methods]
        payment_methods_counts = [p['method_count'] for p in payment_methods]

        # Render the template with analytics data
        analytics_data = {
            'total_users': total_users,
            'total_orders': total_orders,
            'completed_orders': completed_orders,
            'pending_orders': pending_orders,
            'total_revenue': total_revenue,
            'total_products': total_products,
            'total_sold': total_sold,
            'total_recent_orders': total_recent_orders,
            'completed_recent_orders': completed_recent_orders,
            'pending_recent_orders': pending_recent_orders,
            'recent_revenue': recent_revenue,
            'product_names': [p['product_name'] for p in product_stats],
            'product_totals_sold': [p['total_sold'] for p in product_stats],
            'recent_dates': recent_dates,
            'recent_revenue_data': recent_revenue_data,
            'payment_methods_labels': payment_methods_labels,
            'payment_methods_counts': payment_methods_counts
        }

        return render(request, 'dashboard.html', {'analytics_data': analytics_data})
