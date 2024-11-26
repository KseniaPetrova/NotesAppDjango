from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from notes.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', menu_view, name='menu'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page=''), name='logout'),
    path('homenotes/', homenotes_view, name='homenotes'),
    path('delete/<int:note_id>/', delete_note, name='delete_note'),
    path('search/', search_notes, name='search_notes'),

]
"""
    Список маршрутов URL для приложения.
    
    Этот файл определяет все URL-адреса, доступные в приложении, и связывает их с соответствующими представлениями. 
    Каждый маршрут обрабатывает определенный путь и назначает его имени, что позволяет легко ссылаться на него везде в коде приложения.
    
    Маршруты:
    - /admin/ : Панель администратора.
    - / : Основное меню.
    - /register/ : Страница регистрации пользователя.
    - /login/ : Страница входа пользователя.
    - /logout/ : Выход пользователя из системы.
    - /homenotes/ : Страница с домашними заметками пользователя.
    - /delete/<note_id>/ : Удаление заметки по идентификатору.
    - /search/ : Поиск заметок пользователя.
"""