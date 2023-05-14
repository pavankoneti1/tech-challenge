from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import Login
router = DefaultRouter()
# router.register('', Login, basename='login')
urlpatterns = [
    path('', Login.as_view({'get':'list'})),
]