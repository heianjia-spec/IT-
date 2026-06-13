from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.AssetViewSet, basename='asset')

urlpatterns = [
    path('operation-logs/', views.OperationLogViewSet.as_view({'get': 'list'}), name='operation-log-list'),
    path('operation-logs/<int:pk>/', views.OperationLogViewSet.as_view({'get': 'retrieve'}), name='operation-log-detail'),
    path('', include(router.urls)),
]
