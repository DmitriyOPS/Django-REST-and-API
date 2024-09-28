from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Warehouse, Product, User
from .serializers import UserSerializer, WarehouseSerializer, ProductSerializer, ProductCreateSerializer
import sys

# Регистрация пользователя
class RegisterUserView(viewsets.ModelViewSet):
        queryset = User.objects.all()
        permission_classes = [AllowAny]
        serializer_class = UserSerializer

        def post(self, request):
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]

    # Дополнительный эндпоинт для получения продуктов на складе
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def products(self, request, pk=None):
        warehouse = self.get_object()
        serializer = self.get_serializer(warehouse)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Создание склада
class CreateWarehouseView(viewsets.ModelViewSet):

        permission_classes = [AllowAny]
        serializer_class = WarehouseSerializer
        queryset = Warehouse.objects.all()

        def post(self, request):    
            data = request.data.copy()
            serializer = WarehouseSerializer(data=data) 
            if serializer.is_valid(): 
                serializer.save() 
                return Response(serializer.data, status=status.HTTP_201_CREATED) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CreateProductView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        name = data.get('name')  
        quantity = data.get('quantity') 
        
        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            return Response({"error": "Количество должно быть целоым числом."}, status=status.HTTP_400_BAD_REQUEST)
        
        if quantity < 0:
            return Response({"error": "Количество должно быть больше 0."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, существует ли продукт с таким именем
        product = Product.objects.filter(name=name).first()

        if product:
            # Если есть, то увеличиваем количество
            product.quantity += quantity
            product.save()
            return Response(self.get_serializer(product).data, status=status.HTTP_200_OK)
        else:
            # Если товара нет, то создаём
            product = Product.objects.create(name=name, quantity=quantity)
            print(product)
            return Response(self.get_serializer(product).data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

#Поставка товара
class SupplyProductView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    def create(self, request, *args, **kwargs):
        if request.user.role != 'supplier':
            return Response({'error': 'Только поставщики могут поставлять товар'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        product_id = data.get('product')  # Получаем ID продукта
        supply_quantity = data.get('quantity')
        warehouse_id = data.get('warehouse')

        if not product_id or not supply_quantity or not warehouse_id:
            return Response({"error": "ID продукта, количество и склад должны быть указаны"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            supply_quantity = int(supply_quantity)
        except (ValueError, TypeError):
            return Response({"error": "Количество должно быть целым числом"}, status=status.HTTP_400_BAD_REQUEST)

        if supply_quantity <= 0:
            return Response({"error": "Количество должно быть больше 0"}, status=status.HTTP_400_BAD_REQUEST)

    # Получаем продукт по ID
        product = Product.objects.filter(id=product_id).first()
        warehouse = Warehouse.objects.filter(id=warehouse_id).first()
        if not warehouse:
            return Response({"error": "Склад не найден"}, status=status.HTTP_404_NOT_FOUND)
        
        if product:
        # Увеличиваем количество уже существующего продукта
            product.quantity = supply_quantity
            product.warehouse = warehouse
            product.save()
            return Response({
                "success": f"{supply_quantity} units of {product.name} supplied successfully.",
                "remaining_quantity": product.quantity
            }, status=status.HTTP_200_OK)
        else:
        # Если продукт не найден, создаем новый с именем по ID
            warehouse = Warehouse.objects.filter(id=warehouse_id).first()
            if not warehouse:
                return Response({"error": "Склад не найден"}, status=status.HTTP_404_NOT_FOUND)

            new_product = Product.objects.create(name=f"Product {product_id}", quantity=supply_quantity, warehouse=warehouse)
            return Response(self.get_serializer(new_product).data, status=status.HTTP_201_CREATED)


#Получение товара
class RetrieveProductView(viewsets.ModelViewSet): 
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()

    def create(self, request, *args, **kwargs):
        # Проверяем, что запрос делает только потребитель
        if request.user.role != 'consumer':
            return Response({'error': 'Только потребители могут получать товар'}, status=status.HTTP_403_FORBIDDEN)
        print(request.data)
        # Получаем ID продукта из данных запроса
        product_id = request.data.get('product')
        if not product_id:
            return Response({'error': 'ID продукта должно быть указано'}, status=status.HTTP_400_BAD_REQUEST)

        # Ищем продукт по его ID
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)

        # Получаем количество запрашиваемого товара
        try:
            quantity = int(request.data.get('quantity', 0))
        except (ValueError, TypeError):
            return Response({'error': 'Количество должно быть целым числом'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, что запрашиваемое количество больше 0
        if quantity <= 0:
            return Response({'error': 'Количество должно быть больше 0'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, есть ли достаточно товара на складе
        if product.quantity < quantity:
            return Response({'error': 'Количество товара на складе меньше нужного'}, status=status.HTTP_400_BAD_REQUEST)

        # Уменьшаем количество товара
        product.quantity -= quantity
        # Удаляем продукт, если его количество стало 0
        if product.quantity == 0:
            product.delete()
            return Response({
                'success': 'Товар получен и исключён из списка доступных.',
            }, status=status.HTTP_200_OK)
        product.save()

        return Response({
            'success': 'Товар успешно получен.',
            'remaining_quantity': product.quantity
        }, status=status.HTTP_200_OK)
