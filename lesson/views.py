from django.shortcuts import render, redirect
from lesson.forms import ConnexionForm, ProfileForm, LessonForm, SearchForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from lesson.models import Profiles, Lessons, Groups


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
        user = User.objects.get(username=request.user.username)
        profile = Profiles.objects.get(user_id=user.id)
        groups = Groups.objects.filter(profileID=profile.id)
        lessons = []
        for group in groups:
            lesson = group.lessonID
            lessons.append("Vous avez un cours de {}. Le {} de {} à {}".format(lesson.nom, lesson.date, lesson.begin,
                                                                               lesson.end))
        context = {
            'messages': lessons
        }
        return render(request, 'home.html', context)

    else:
        return redirect('/')


def add(request):
    if request.user.is_authenticated:
        lessonform = LessonForm()
        context = {
            'lessonform': lessonform
        }
        if request.method == 'POST':
            form = LessonForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                room = form.cleaned_data['room']
                date = form.cleaned_data['date']
                begin = form.cleaned_data['begin']
                end = form.cleaned_data['end']
                promo = form.cleaned_data['promo']
                campus = form.cleaned_data['campus']
                subject = form.cleaned_data['subject']
                lesson = Lessons(nom=name, date=date, sujet=subject, promo=promo, begin=begin, campus=campus, end=end,
                                 salle=room)
                lesson.save()
                user = User.objects.get(username=request.user.username)
                profile = Profiles.objects.get(user_id=user.id)
                group = Groups(profileID=profile, lessonID=lesson, teacher=True)
                group.save()
        return render(request, 'add.html', context)

    else:
        return redirect('/')


def search(request):
    if request.user.is_authenticated:
        searchform = SearchForm()
        context = {
            'searchform': searchform
        }
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                date = form.cleaned_data['date']
                promo = form.cleaned_data['promo']
                campus = form.cleaned_data['campus']
                finds = Lessons.objects.all()
                if name != "":
                    finds = finds.filter(nom=name)
                if date is not None:
                    finds = finds.filter(date=date)
                if promo != "":
                    finds = finds.filter(promo=promo)
                if campus != "":
                    finds = finds.filter(campus=campus)
                context['lessons'] = finds

        return render(request, 'search.html', context)

    else:
        return redirect('/')


def subscribe(request, lesson_id):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        profile = Profiles.objects.get(user_id=user.id)
        lesson = Lessons.objects.get(id=lesson_id)
        group = Groups.objects.filter(lessonID=lesson)
        if len(group) > 5:
            context = {
                'disponible': False
            }
        else:
            already = False
            for person in group:
                if person.profileID == profile:
                    print("déjà inscrit")
                    already = True
                    context = {
                        'already': True
                    }

            if not already:
                context = {
                    'disponible': True
                }
                subscriber = Groups(lessonID=lesson, profileID=profile)
                subscriber.save()

        return render(request, 'subscribe.html', context)

    else:
        return redirect('/')


def view_logout(request):
    logout(request)
    return redirect('/')
