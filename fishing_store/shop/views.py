from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, UserRegistrationSerializer
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model

User = get_user_model()  # Получаем модель пользователя

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Доступно всем пользователям

class CustomTokenObtainPairView(TokenObtainPairView):
    # Можешь добавить свои дополнительные поля в ответ токена
    pass