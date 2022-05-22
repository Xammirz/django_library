
from django import forms


class BookSearch(forms.Form):
    search = forms.CharField(
        label="Книга", required=False, widget=forms.TextInput(attrs={'class': "field__input", 'id': 'search', 'autofocus': True}))
    author = forms.CharField(
        label="Автор", required=False, widget=forms.TextInput(attrs={'class': "field__input", 'id': 'author'}))