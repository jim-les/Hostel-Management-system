# rent/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('record_meal/', views.record_meal, name='record_meal'),
    # path('post_query/', views.post_query, name='post_query'),
    # path('make_payment/', views.make_payment, name='make_payment'),
]
