from django.urls import path
from .views import CreateToken

urlpatterns = [
    path('token/', CreateToken.as_view(), name='login'),
]