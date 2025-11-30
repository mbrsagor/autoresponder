from django import forms
from user.models import Supplier


class SupplierModelForm(forms.ModelForm):
    class Meta:
        model = Supplier
        read_only_fields = ('store',)
        fields = (
            'name', 'phone', 'email', 'is_active',
            'address', 'contact_person'
        )
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'is_active'}),
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Enter supplier name'}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'phone', 'placeholder': 'Enter supplier phone'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'Enter supplier email'}),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'address', 'placeholder': 'Enter supplier address'}),
            'contact_person': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'avatar', 'placeholder': 'Enter contact person name'}),
        }
