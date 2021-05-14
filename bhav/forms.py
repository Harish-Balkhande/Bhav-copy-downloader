from django import forms

class search_form(forms.Form):
    search_key = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder':'Enter Code or Name'}))
    
    