from django import forms
from django.core.exceptions import ValidationError

from .models import *


class AddGoodForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Не выбрано'

    class Meta:
        model = Clothes
        fields = ['title', 'slug', 'content', 'photo', 'price', 'gender', 'is_published', 'brand', 'category',
                  'subcategory']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if len(title) > 200:
    #         raise ValidationError('Длина превышает 200 символов')
    #     return title
