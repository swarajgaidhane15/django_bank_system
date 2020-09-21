from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Profile, Transaction
from .forms import NewUserForm, EditProfile, AddTransaction


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


# Displays the transactions of the logged in account
@login_required
def trasactionList(request, pk):
    trans = Transaction.objects.filter(account=pk)
    return render(request, "bank/transactions.html", {"transactions": trans})


# Add Transaction
class AddTransaction(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Transaction
    fields = ['amount', 'description', 'trans_type']
    template_name = "bank/create_trans.html"
    success_message = "Transaction made successfully"

    def form_valid(self, form):
        form.instance.account = self.request.user
        return super().form_valid(form)


# Delete a transaction
@login_required
def delete_transaction(request, trans_id):
    trans = Transaction.objects.get(pk=trans_id)
    trans.delete()
    return redirect("bank:transactions", request.user.id)


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
            messages.success(
                request, f"Rs. 100 have been credited to your account as bonus : )")
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
