from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, UserRegistrationSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .permissions import IsAdminOrReadOnly  # Импортируем новый класс прав

User = get_user_model()  # Получаем модель пользователя

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Получаем токены
        tokens = serializer.validated_data
        
        # Получаем пользователя из сериализованных данных
        user = serializer.user
        
        # Формируем ответ с токенами и дополнительными полями
        return Response({
            'access': tokens['access'],
            'refresh': tokens['refresh'],
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
        })