from django.urls import path
from .views import index

app_name = 'socketio_app'

urlpatterns = [
    # User Register URL
    path('index/', index, name='index'),
]
