from django import forms
from .models import Voucher

class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = ['code', 'discount_amount', 'expiration_date', 'is_percentage']
