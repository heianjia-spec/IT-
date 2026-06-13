from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('alert-rules', views.AlertRuleViewSet, basename='alert-rule')
router.register('alert-logs', views.AlertLogViewSet, basename='alert-log')
router.register('email-config', views.EmailConfigViewSet, basename='email-config')

urlpatterns = [
    path('email-template/', views.EmailTemplateViewSet.as_view({'get': 'list', 'post': 'create'}), name='email-template'),
    path('', include(router.urls)),
]
