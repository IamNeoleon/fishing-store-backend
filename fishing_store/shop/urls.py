from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminOrderViewSet, BrandViewSet, CartItemViewSet, CartViewSet, CategoryViewSet, OrderViewSet, ProductViewSet, UserOrdersViewSet, UserRegistrationView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cart-items')
router.register(r'brands', BrandViewSet, basename='brands')
router.register(r'admin/orders', AdminOrderViewSet, basename='admin-orders')  # Роут для админов
router.register(r'orders', OrderViewSet, basename='orders')  # Роут для пользователей

urlpatterns = [
    path('', include(router.urls)),
	path('register/', UserRegistrationView.as_view(), name='user-register'),
	path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('categories/<int:pk>/subcategories/', CategoryViewSet.as_view({'get': 'get_subcategories'}), name='category-subcategories'),  # Новый путь
]
