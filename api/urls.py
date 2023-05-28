from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

v1_router = DefaultRouter()
v1_router.register(r'transaction',
                   views.TransactionViewSet,
                   basename='transactions')

urlpatterns = [
    path('', include(v1_router.urls), ),
]
