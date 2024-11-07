from django.urls import path
from .views import (
    RegisterView, LoginView, ProfileView, UpdateProfileView,
    ProductListView, ProductDetailView, ProductSearchView, AddProductView,
    UpdateProductView, DeleteProductView, AddToCartView, CartView,
    RemoveFromCartView, CheckoutView, OrderDetailView, InitiatePaymentView,
    VerifyPaymentView, PaymentHistoryView, TrackOrderView, AssignDeliveryPartnerView,
    UpdateDeliveryStatusView
)

urlpatterns = [
    # A. User Management and Authentication
    path('users/register/', RegisterView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/profile/', ProfileView.as_view(), name='profile'),
    path('users/profile/update/', UpdateProfileView.as_view(), name='update_profile'),

    # B. Product Management
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/search/', ProductSearchView.as_view(), name='product_search'),
    path('admin/products/', AddProductView.as_view(), name='add_product'),
    path('admin/products/<int:pk>/', UpdateProductView.as_view(), name='update_product'),
    path('admin/products/<int:pk>/delete/', DeleteProductView.as_view(), name='delete_product'),

    # C. Cart and Checkout
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='view_cart'),
    path('cart/<int:productId>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('orders/checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/<int:orderId>/', OrderDetailView.as_view(), name='order_detail'),

    # D. Payment Integration
    path('payments/initiate/', InitiatePaymentView.as_view(), name='initiate_payment'),
    path('payments/verify/', VerifyPaymentView.as_view(), name='verify_payment'),
    path('payments/history/', PaymentHistoryView.as_view(), name='payment_history'),

    # E. Delivery Management
    path('orders/<int:orderId>/track/', TrackOrderView.as_view(), name='track_order'),
    path('orders/<int:orderId>/assign/', AssignDeliveryPartnerView.as_view(), name='assign_delivery_partner'),
    path('delivery/update-status/', UpdateDeliveryStatusView.as_view(), name='update_delivery_status'),
]
