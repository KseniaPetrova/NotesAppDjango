from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Note
import re  # Pегулярные выражения


class UserRegistrationForm(forms.ModelForm):
    """
    Форма для регистрации нового пользователя.

    Поля формы:
    - username: Логин пользователя (максимум 30 символов).
    - password: Пароль пользователя, вводимый в защищенном режиме.
    - password_confirm: Подтверждение пароля, вводимое в защищенном режиме.
    - email: Адрес электронной почты пользователя.
    - phone: Номер телефона, обязательное поле, формат: +7XXXXXXXXXX.

    Валидация:
    - Проверяет, совпадают ли пароли.
    - Проверяет, что имя пользователя уникально.
    - Проверяет корректность формата номера телефона (должен содержать 11 цифр).

    Методы:
    - clean_password_confirm: Непосредственная проверка совпадения паролей.
    - clean_username: Проверка на уникальность имени пользователя.
    - clean_phone: Валидация формата номера телефона.
    - save: Сохраняет нового пользователя в базе данных, устанавливая зашифрованный пароль.

    Примечание: Если параметр commit равен True, пользователь сохраняется в базе данных, иначе объект пользователя возвращается без сохранения.
    """
    username = forms.CharField(max_length=30, label="Введите логин")
    password = forms.CharField(widget=forms.PasswordInput(), label="Введите пароль")
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Повторите пароль")
    email = forms.EmailField()
    phone = forms.CharField(max_length=15, required=True, label='Номер телефона',
                            widget=forms.TextInput(attrs={'placeholder': '+7XXXXXXXXXX'}))

    class Meta:
        model = User
        fields = ['username', 'phone', 'email', 'password', 'password_confirm']  # Порядок полей отображаемых в форме

    def clean_password_confirm(self):
        """Проверка совпадения паролей. Возвращает пароль """
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise ValidationError("Пароли не совпадают!")
        return password_confirm

    def clean_username(self):
        """Проверка на уникальность имени пользователя."""
        username = self.cleaned_data.get('username')
        lowercase_username = username.lower()
        if User.objects.filter(username=lowercase_username).exists():
            raise ValidationError("Данный логин уже занят.")
        return lowercase_username

    def clean_phone(self):
        """Валидация формата номера телефона."""
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+?[0-9]{11}$', phone):
            raise ValidationError("Введите корректный номер телефона.")
        return phone

    def save(self, commit=True):  # Этот параметр указывает, следует ли действительно сохранять объект пользователя в базе данных
        """Сохраняет нового пользователя в базе данных, устанавливая зашифрованный пароль."""
        user = super(UserRegistrationForm, self).save(commit=False)  # Создает эксемпляр пользователя и не дает его сразу сохранить
        user.set_password(self.cleaned_data["password"])  # Хранить пароль в зашифрованном виде
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """
    Кастомизированная форма аутентификации пользователя.

    Этот класс расширяет стандартную форму аутентификации Django,
    предоставляя возможность настройки механизмов аутентификации
    пользователя.

    Поля формы:
    - username: Логин пользователя.
    - password: Пароль пользователя.
    """
    class Meta:
        model = AuthenticationForm
        fields = ('username', 'password')
        labels = {
            'username': 'Логин',
            'password': 'Пароль',
        }


class NoteForm(forms.ModelForm):
    """
        Форма для создания и редактирования заметки.

        Эта форма основана на модели Note и предоставляет поля
        для ввода заголовка и содержания заметки. Поля содержат
        определенные виджеты для улучшения пользовательского интерфейса.

        Атрибуты:
            title (str): Заголовок заметки.
            content (str): Содержание заметки.
    """
    class Meta:
        model = Note
        fields = ['title', 'content']  # Поля, которые мы хотим использовать в форме
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Заголовок'}),
            'content': forms.Textarea(),
        }