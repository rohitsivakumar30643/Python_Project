from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Loan, Payment
from .forms import LoanForm, PaymentForm, RegisterForm
from .utils import calculate_emi

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = False
            user.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "loanapp/register.html", {"form": form})

@login_required
def dashboard(request):
    loans = Loan.objects.all() if request.user.is_staff else Loan.objects.filter(borrower=request.user)
    context = {
        "loans": loans,
        "total_loans": loans.count(),
        "approved_loans": loans.filter(status='APPROVED').count(),
        "closed_loans": loans.filter(status='CLOSED').count(),
        "total_collected": sum(loan.total_paid() for loan in loans),
    }
    return render(request, "loanapp/dashboard.html", context)

@login_required
def apply_loan(request):
    if request.user.is_staff: return redirect("dashboard")
    if request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.borrower = request.user
            loan.emi = calculate_emi(loan.amount, loan.interest_rate, loan.tenure_months)
            loan.status = 'PENDING'
            loan.save()
            return redirect("dashboard")
    else:
        form = LoanForm()
    return render(request, "loanapp/apply_loan.html", {"form": form})

@login_required
def loan_detail(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    return render(request, "loanapp/loan_detail.html", {"loan": loan, "payments": loan.payments.all()})

@login_required
def make_payment(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if loan.borrower != request.user or loan.status != 'APPROVED':
        return redirect("dashboard")

    m_interest = loan.get_monthly_interest()
    t_close = round(loan.remaining_balance() + m_interest, 2)

    if request.method == "POST":
        form = PaymentForm(request.POST, loan=loan)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.loan = loan
            payment.save()

            if loan.remaining_balance() <= 0:
                loan.status = 'CLOSED'
                loan.save()
                messages.success(request, "Loan fully paid and closed!")
            return redirect("loan_detail", pk=pk)
    else:
        form = PaymentForm(loan=loan)

    return render(request, "loanapp/make_payment.html", {
        "form": form, "loan": loan,
        "monthly_interest": m_interest,
        "total_to_close": t_close
    })

@staff_member_required
def approve_loan(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    loan.status = 'APPROVED'
    loan.save()
    return redirect("dashboard")

@staff_member_required
def reject_loan(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    loan.status = 'REJECTED'
    loan.save()
    return redirect("dashboard")
