from rest_framework import serializers
from .models import User, Warehouse, Product
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        print("User save:", user)
        return user


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    
    class Meta:
        model = Product
        fields = ['name', 'quantity']

class WarehouseSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)  

    class Meta:
        model = Warehouse
        fields = ['name', 'products']  
    
    def validate_name(self, value):
        if Warehouse.objects.filter(name=value).exists():
            raise serializers.ValidationError("Склад с таким названием уже есть")
        return value


class ProductCreateSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='name'  
    )
    quantity = serializers.IntegerField()
    warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(),
        required=True
    )

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Количество должно быть больше 0")
        return value


    

