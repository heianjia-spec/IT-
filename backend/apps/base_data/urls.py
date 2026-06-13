from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('categories', views.AssetCategoryViewSet, basename='category')
router.register('departments', views.DepartmentViewSet, basename='department')
router.register('locations', views.LocationViewSet, basename='location')
router.register('suppliers', views.SupplierViewSet, basename='supplier')

urlpatterns = [
    path('', include(router.urls)),
]
