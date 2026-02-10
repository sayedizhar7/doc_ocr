from django.urls import path
from .views import dashboard, result

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("result/<int:pk>/", result, name="result"),
]
