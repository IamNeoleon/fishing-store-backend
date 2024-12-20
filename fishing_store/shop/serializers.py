from rest_framework import serializers
from .models import Brand, Category, Product, Cart, CartItem, Order, OrderItem
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        data['is_staff'] = self.user.is_staff

        return data
    
class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'subcategories']
  
class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'available', 'category', 'brand', 'brand_name', 'created_at', 'updated_at', 'image']

    def to_representation(self, instance):
        """Добавляем отладочный вывод перед возвратом данных"""
        representation = super().to_representation(instance)
        print(f"[DEBUG] Serialized Product Data: {representation}")
        return representation

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name', 'price', 'image']  # Указываем только нужные поля

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)  
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)  

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'product_id']  

    def create(self, validated_data):
        product = validated_data.pop('product_id')
        cart_item = CartItem.objects.create(product=product, **validated_data)  
        return cart_item

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']
        
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'total_amount', 'address', 'personal_info', 'status', 'items']