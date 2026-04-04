from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class PoolForm(forms.Form):
    name = forms.CharField(
        label='Ваше имя',
        min_length=3,
        max_length=50,
        required=True
    )
    
    rating = forms.ChoiceField(
        label='Оценка сайта',
        choices=[(5, '5 - Отлично'), (4, '4 - Хорошо'), (3, '3 - Нормально'), (2, '2 - Плохо'), (1, '1 - Ужасно')],
        widget=forms.RadioSelect,
        initial=5
    )
    
    usability = forms.ChoiceField(
        label='Удобство использования',
        choices=[('Удобно', 'Удобно'), ('Нормально', 'Нормально'), ('Сложно', 'Сложно')],
        required=True
    )
    
    features = forms.MultipleChoiceField(
        label='Что вам понравилось? (можно выбрать несколько)',
        choices=[('Дизайн', 'Дизайн'), ('Содержание', 'Содержание'), ('Быстрая работа', 'Быстрая работа'), ('Удобное меню', 'Удобное меню')],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    recommendations = forms.ChoiceField(
        label='Рекомендуете ли вы сайт?',
        choices=[('Да', 'Да'), ('Нет', 'Нет'), ('Возможно', 'Возможно')],
        widget=forms.RadioSelect,
        required=True
    )
    
    message = forms.CharField(
        label='Ваши пожелания и замечания',
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        required=False
    )
    
    contact = forms.BooleanField(
        label='Согласен на получение новостей сайта',
        required=False
    )

class BootstrapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'
                               }))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Пароль'
                               }))