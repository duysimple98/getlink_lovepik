from django import forms

class SearchForm(forms.Form):
    look = forms.CharField(label=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập link cần get'}))