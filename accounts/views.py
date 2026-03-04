from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                password=password,
                username=email,  # Set username to email for compatibility with authentication
            )
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        # Handle login logic here (e.g., form validation, user authentication)
        pass
    return render(request, 'accounts/login.html')

def logout(request):
    return render(request, 'accounts/logout.html')
