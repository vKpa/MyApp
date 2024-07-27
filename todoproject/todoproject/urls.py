from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from todo import views as todo_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='todo/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', todo_views.register, name='register'),
    path('', include('todo.urls')),
]