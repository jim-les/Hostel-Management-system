from django.urls import include, path
# from django.contrib.auth import views as auth_views
from .views import login_view, logout_view

urlpatterns = [
    
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    
]