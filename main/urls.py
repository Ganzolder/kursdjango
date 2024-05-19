from django.urls import path
from main.apps import MainConfig
from main.views import home

app_name = MainConfig.name

urlpatterns = [
    path('', home, name='index.html'),
]
