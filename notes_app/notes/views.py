from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, CustomAuthenticationForm, NoteForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpRequest, HttpResponse
from .models import Note
from django.db.models import Q  # Позволяет условно объединять выражения
# Create your views here.


def menu_view(request: HttpRequest) -> HttpResponse:
    """
        Отображает главную страницу.

        Параметры:
            request (HttpRequest): Объект HTTP-запроса.

        Возвращает:
            HttpResponse: Ответ с отрисованной главной страницей.
    """
    return render(request, 'menu.html')


def register(request: HttpRequest) -> HttpResponse:
    """
        Регистрация нового пользователя.

        Если пользователь уже авторизован, происходит перенаправление
        на домашнюю страницу. В противном случае отображается форма
        регистрации, и, при успешной отправке формы, пользователь
        авторизуется и перенаправляется на домашнюю страницу.

        Параметры:
            request (HttpRequest): Объект HTTP-запроса.

        Возвращает:
            HttpResponse: Ответ с отрисованной страницей регистрации.
    """
    if request.user.is_authenticated:
        return redirect('homenotes')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homenotes')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request: HttpRequest) -> HttpResponse:
    """
        Вход пользователя на сайт.

        Если пользователь уже авторизован, происходит перенаправление
        на домашнюю страницу. В противном случае отображается форма
        входа, и, при успешной отправке формы, пользователь авторизуется
        и перенаправляется на домашнюю страницу.

        Параметры:
            request (HttpRequest): Объект HTTP-запроса.

        Возвращает:
            HttpResponse: Ответ с отрисованной страницей входа.
    """
    if request.user.is_authenticated:
        return redirect('homenotes')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = request.POST.get('remember_me')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                if remember_me:
                    request.session.set_expiry(None)  # Сессия будет действительна до выхода
                else:
                    request.session.set_expiry(0)  # Сеанс завершится при закрытии браузера

                return redirect('homenotes')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def homenotes_view(request: HttpRequest) -> HttpResponse:
    """
        Отображает домашние заметки пользователя.

        Пользователь может создавать, редактировать и просматривать свои заметки.

        Параметры:
            request (HttpRequest): Объект HTTP-запроса.

        Возвращает:
            HttpResponse: Ответ с отрисованной страницей домашних заметок.
    """
    notes = Note.objects.filter(author=request.user).order_by('-updated_at')
    selected_note = None

    note_id = request.GET.get('note_id')
    if note_id:
        selected_note = get_object_or_404(Note, id=note_id, author=request.user)

    if request.method == 'POST':
        if 'note_id' in request.POST:  # Обработка редактирования заметки
            note = get_object_or_404(Note, id=request.POST['note_id'], author=request.user)
            note.title = request.POST['title']
            note.content = request.POST['content']
            note.save()
            return redirect('homenotes')
        else:  # Обработка создания заметки
            note = Note(author=request.user, title=request.POST['title'], content=request.POST['content'])
            note.save()
            return redirect('homenotes')

    return render(request, 'homenotes.html', {'notes': notes, 'selected_note': selected_note})


@login_required
def delete_note(request: HttpRequest, note_id: int) -> HttpResponse:
    """
    Удаление заметки пользователя.

    Если пользователь подтверждает удаление заметки, она будет удалена
    и пользователь перенаправляется на домашнюю страницу.

    Параметры:
        request (HttpRequest): Объект HTTP-запроса.
        note_id (int): Идентификатор заметки, которую необходимо удалить.

    Возвращает:
        HttpResponse: Ответ с отрисованной страницей домашних заметок.
    """
    note = get_object_or_404(Note, id=note_id, author=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('homenotes')

    return render(request, 'homenotes.html', {'note_to_delete': note})


@login_required
def search_notes(request: HttpRequest) -> HttpResponse:
    """
        Поиск заметок пользователя.

        Позволяет пользователю искать свои заметки по заголовку или содержимому.

        Параметры:
            request (HttpRequest): Объект HTTP-запроса.

        Возвращает:
            HttpResponse: Ответ с отрисованной страницей поиска заметок.
    """
    query = request.GET.get('Поиск', '').strip()
    notes = Note.objects.filter(author=request.user)

    if query:
        notes = notes.filter(Q(title__icontains=query) | Q(content__icontains=query))

    form = NoteForm()  # Не забываем передать форму
    return render(request, 'search.html', {'notes': notes, 'form': form, 'query': query})