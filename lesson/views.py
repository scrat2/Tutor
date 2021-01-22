from django.shortcuts import render, redirect
from lesson.forms import ConnexionForm, ProfileForm, LessonForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
from lesson.models import Profiles


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
                # Check if IDs are good
                user = authenticate(username=username, password=password)
                if user is not None:
                    # If good log user and check the profil create it if needed
                    profile = Profiles.objects.filter(user=user)
                    if not profile.exists():
                        profile = Profiles(user=user)
                        profile.save()
                    login(request, user)
                    return redirect('/home')
                else:
                    context['log'] = False

        return render(request, 'connexion.html', context)


def profil(request):
    if request.user.is_authenticated:
        form = ProfileForm()
        context = {
            'form': form
        }
        user = User.objects.get(username=request.user.username)
        profile = Profiles.objects.get(user_id=user.id)
        context['nbr_heure'] = profile.nbr_heure
        if request.method == 'POST':
            # Get data from the form
            form = ProfileForm(request.POST)
            # Clean data to avoid injection
            if form.is_valid():
                promo = form.cleaned_data['promo']
                campus = form.cleaned_data['campus']
                if promo != "":
                    profile.promo = promo
                if campus != "":
                    profile.campus = campus
                profile.save()

        return render(request, 'profil.html', context)

    else:
        return redirect('/')


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')

    else:
        return redirect('/')


def add(request):
    if request.user.is_authenticated:
        userform = ProfileForm()
        lessonform = LessonForm()
        context = {
            'userform': userform,
            'lessonform': lessonform
        }
        return render(request, 'add.html', context)

    else:
        return redirect('/')


def search(request):
    if request.user.is_authenticated:
        return render(request, 'search.html')

    else:
        return redirect('/')


def view_logout(request):
    logout(request)
    return redirect('/')
