from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Brand, Category, Product, Cart, CartItem
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer, UserRegistrationSerializer, CustomTokenObtainPairSerializer, CartSerializer, CartItemSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .permissions import IsAdminOrReadOnly  # Импортируем новый класс прав
from django_filters.rest_framework import DjangoFilterBackend  # Импортируем DjangoFilterBackend
from django_filters import rest_framework as filters  # Импортируем фильтры
from rest_framework import filters as drf_filters  # Импортируем фильтры из DRF

User = get_user_model()  # Получаем модель пользователя



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    def get_subcategories(self, request, pk=None):
        try:
            category = self.get_object()  # Получаем категорию по ID (pk)
            subcategories = category.subcategories.all()  # Получаем подкатегории
            serializer = CategorySerializer(subcategories, many=True)  # Сериализуем подкатегории
            return Response(serializer.data)  # Возвращаем данные подкатегорий
        except Category.DoesNotExist:
            return Response({"detail": "Category not found."}, status=404)

class ProductFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = filters.NumberFilter(field_name="price", lookup_expr='lte')
    brand = filters.BaseInFilter(field_name='brand', lookup_expr='in')  # Для фильтрации по нескольким брендам

    class Meta:
        model = Product
        fields = ['price_min', 'price_max', 'brand', 'category']  # Указываем доступные фильтры

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter]  # Используем DRF фильтр
    filterset_class = ProductFilter
    ordering_fields = ['price']  # Поля для сортировки
    ordering = ['price']

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category')
        print(f"[DEBUG] Category ID from request: {category_id}")

        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                print(f"[DEBUG] Fetched Category: {category.name}, Parent: {category.parent}")
                
                if category.parent is None:  
                    subcategory_ids = category.subcategories.values_list('id', flat=True)
                    print(f"[DEBUG] Subcategory IDs for parent category '{category.name}': {list(subcategory_ids)}")
                    
                    all_category_ids = [category.id] + list(subcategory_ids)
                    print(f"[DEBUG] All Category IDs to filter products: {all_category_ids}")
                    
                    queryset = queryset.filter(category__id__in=all_category_ids)
                else:
                    queryset = queryset.filter(category=category)
            except Category.DoesNotExist:
                print("[DEBUG] Category not found, returning empty queryset.")
                queryset = Product.objects.none()

        print(f"[DEBUG] Final Queryset Product Count: {queryset.count()}")
        for product in queryset:
            print(f"[DEBUG] Product in Queryset: ID={product.id}, Name={product.name}, Category={product.category}")

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        print(f"[DEBUG] Manual Serialization Data: {serializer.data}")  # Отладка для проверки данных
        return Response(serializer.data)  # Возвращаем ответ напрямую

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
        
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        return Response(CartSerializer(cart).data)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)
        
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]  # Или другая политика, которую вы используете
