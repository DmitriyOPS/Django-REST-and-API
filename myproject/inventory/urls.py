from rest_framework.routers import DefaultRouter
from django.urls import path
from inventory.views import (
    RegisterUserView,
    CreateWarehouseView,
    CreateProductView,
    SupplyProductView,
    RetrieveProductView,
    WarehouseViewSet
)

router = DefaultRouter()
router.register('create_warehouse', CreateWarehouseView, basename='create_warehouse')
router.register('create_product', CreateProductView, basename='create_product')
router.register('supply_product', SupplyProductView, basename='supply_product')
router.register('retrieve_product', RetrieveProductView, basename='retrieve_product')
router.register('register',RegisterUserView,basename='register')
router.register(r'warehouse', WarehouseViewSet)

urlpatterns = [
    
]

urlpatterns.extend(router.urls)