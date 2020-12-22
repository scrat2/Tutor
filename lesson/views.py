import ldap
from django_auth_ldap.backend import LDAPBackend
from django.shortcuts import render, redirect
from lesson.forms import ConnexionForm
from django.contrib.auth import authenticate, login


# Create your views here.


def connexion(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        # Get the form from forms.py and add it to the context to send it to the template.
        form = ConnexionForm()
        context = {
            'form': form
        }
        if request.method == 'POST':
            # Get data from the form
            form = ConnexionForm(request.POST)
            # Clean data to avoid injection
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/home')
                else:
                    context['log'] = False

        return render(request, 'connexion.html', context)


def profil(request):
    if request.user.is_authenticated:
        return render(request, 'profil.html')

    else:
        return redirect('/')


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')

    else:
        return redirect('/')


def add(request):
    if request.user.is_authenticated:
        return render(request, 'add.html')

    else:
        return redirect('/')


def search(request):
    if request.user.is_authenticated:
        return render(request, 'search.html')

    else:
        return redirect('/')
