from django import forms
from .models import Loan, Payment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['amount', 'interest_rate', 'tenure_months']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'tenure_months': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount_paid']
        widgets = {'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})}

    def __init__(self, *args, **kwargs):
        self.loan = kwargs.pop('loan', None)
        super().__init__(*args, **kwargs)

    def clean_amount_paid(self):
        amount = self.cleaned_data.get('amount_paid')
        if self.loan:
            # Allow: Current Principal + Interest + 10 rupees safety buffer
            limit = self.loan.remaining_balance() + self.loan.get_monthly_interest() + 10
            if amount > limit:
                raise forms.ValidationError(f"Payment exceeds limit. Max allowed: {round(limit, 2)}")
        return amount

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']