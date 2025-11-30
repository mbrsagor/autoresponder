from django import forms
from user.models import Customer


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        read_only_fields = ('store',)
        fields = (
            'name', 'phone', 'email', 'is_active',
            'address', 'avatar'
        )
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'is_active'}),
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Enter customer name'}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'phone', 'placeholder': 'Enter customer phone'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'Enter customer email'}),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'address', 'placeholder': 'Enter customer address'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'id': 'avatar'}),
        }
