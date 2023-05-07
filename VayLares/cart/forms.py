from django import forms


class CartAddProductForm(forms.Form):

    def __init__(self, count, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].choices = [(i, str(i)) for i in range(1, count + 1)]

    quantity = forms.TypedChoiceField(coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


