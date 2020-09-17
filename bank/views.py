from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Profile, Transaction
from .forms import NewUserForm, EditProfile, AddTransaction


# Displays the transactions of the logged in account
class TransactionsList(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "bank/transactions.html"
    context_object_name = "transactions"
    ordering = ["-trans_date"]


# Details of logged in user
@login_required
def profile(request):
    return render(request, "bank/profile.html")


# Update profile
@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = EditProfile(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(
                request, "Your changes have been updated successfully !")
            return redirect("bank:profile")
        else:
            messages.info(request, "Please correct the errors below.")
    else:
        user_form = EditProfile(instance=request.user)

    return render(request, "bank/update_profile.html", {"form": user_form})


# Add Transaction
@login_required
def add_trans(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        add_form = AddTransaction(request.POST)
        if add_form.is_valid():
            create_trans = add_form.save(commit=False)
            create_trans.account = user
            amount = add_form.cleaned_data.get('amount')
            trans_type = add_form.cleaned_data.get('trans_type')
            if trans_type == 'Withdraw':
                user.profile.account_balance -= amount
            else:
                user.profile.account_balance += amount
            create_trans.save()
            messages.success(
                request, f"Rs. {amount} have been {trans_type}ed !")
            return redirect("bank:transactions", user_id)
        else:
            messages.info(request, "Please correct the errors below.")
    else:
        add_form = AddTransaction()

    return render(request, "bank/create_trans.html", {"form": add_form})


# Delete a transaction
@login_required
def delete_transaction(request, trans_id):
    trans = Transaction.objects.get(pk=trans_id)
    trans.delete()
    return redirect("bank:profile")


# Register user
def register(request):
    if request.method == 'POST':
        form = NewUserForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('first_name')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            return redirect("bank:profile")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = NewUserForm
    return render(request,
                  "bank/register.html",
                  context={"form": form})


# Logout user
@login_required
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully !!")
    return redirect("bank:login")
