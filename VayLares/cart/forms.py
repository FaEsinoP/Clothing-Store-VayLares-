from django import forms

VARIANTS = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=VARIANTS, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)