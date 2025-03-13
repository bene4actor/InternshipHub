import re
from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError

from .models import Intern


class InternshipForm(forms.Form):
    start_date = forms.DateField(label='Дата начала', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='Дата окончания', widget=forms.DateInput(attrs={'type': 'date'}))
    full_name = forms.CharField(max_length=255, label='Полное имя')
    contact_info = forms.CharField(max_length=255, label='Контактная информация')
    email = forms.EmailField(label='Электронная почта')


class InternAdminForm(forms.ModelForm):
    class Meta:
        model = Intern
        fields = "__all__"

    def clean(self):
        inn = self.cleaned_data.get("INN")
        birth_date = self.cleaned_data.get("birth_date")

        if not birth_date:
            raise forms.ValidationError("Дата рождения не указана.")

        # Проверка ИНН: он должен состоять из 14 цифр
        if not inn or len(inn) != 14 or not inn.isdigit():
            raise forms.ValidationError("ИНН должен состоять ровно из 14 цифр.")

        # Проверка на совпадение даты рождения из ИНН
        inn_birth_date = f'{inn[5:9]}-{inn[3:5]}-{inn[1:3]}'
        print(inn_birth_date)

        try:
            inn_birth_date_obj = datetime.strptime(inn_birth_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError("Невозможно преобразовать дату рождения из ИНН.")

        # Сравнение дат
        if birth_date != inn_birth_date_obj:
            raise ValidationError("Дата рождения из ИНН не совпадает с указанной датой рождения.")

        return self.cleaned_data


