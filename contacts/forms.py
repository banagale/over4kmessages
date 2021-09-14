from django import forms

from contacts.models import Contact


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'First',
               'autocomplete': 'given-name'}))

    class Meta:
        model = Contact
        fields = ['first_name']
        widgets = {
            'first_name': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control', 'placeholder': '',
                       'autocomplete': 'username'}),
        }
