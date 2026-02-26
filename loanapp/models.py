from django.db import models
from django.contrib.auth.models import User

class Loan(models.Model):
    STATUS_CHOICES = [('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('CLOSED', 'Closed')]
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    interest_rate = models.FloatField()
    tenure_months = models.IntegerField()
    emi = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_paid(self):
        # Sums all payments (Interest + Principal)
        return sum(payment.amount_paid for payment in self.payments.all())

    def remaining_balance(self):
        # Principal minus total payments received
        balance = self.amount - self.total_paid()
        return max(balance, 0)

    def get_monthly_interest(self):
        # Interest based on current outstanding principal
        interest = (self.remaining_balance() * (self.interest_rate / 100)) / 12
        return round(interest, 2)

    def __str__(self):
        return f"Loan {self.id} - {self.borrower.username}"

class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="payments")
    amount_paid = models.FloatField()
    payment_date = models.DateField(auto_now_add=True)