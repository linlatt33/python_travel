from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Places, Topic, Message, User
from .form import PlaceForm, UserForm, MyUserCreateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponse


# Create your views here.


def loginpage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password Does not Exist')
    context = {'page': page}
    return render(request, 'place/login_register.html', context)


def logoutpage(request):
    logout(request)
    return redirect('home')


def registerpage(request):
    registerform = MyUserCreateForm()

    if request.method == 'POST':
        form = MyUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during register')
    context = {'registerform': registerform}
    return render(request, 'place/login_register.html', context)


@login_required(login_url='/login')
def home(request):
    q = request.GET.get('q') \
        if request.GET.get('q') != None \
        else ''
    places = Places.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(located__icontains=q)
    )
    topics = Topic.objects.all()[0:3]
    comments = Message.objects.filter(Q(place__topic__name__icontains=q))
    context = {'places': places, 'topics': topics, 'comments': comments}
    return render(request, 'place/home.html', context)


@login_required(login_url='/login')
def place(request, pk):
    place = Places.objects.get(id=pk)
    comments = place.message_set.all()
    participants = place.participants.all()
    if request.method == "POST":
        comment = Message.objects.create(
            user=request.user,
            place=place,
            order_hotel=request.POST.get('comment')
        )
        place.participants.add(request.user)
        return redirect('places', pk=place.id)
    context = {'place': place, 'comments': comments, 'participants': participants}
    return render(request, 'place/place.html', context)


def userprofile(request, pk):
    user = User.objects.get(id=pk)
    places = user.places_set.all()
    comments = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'places': places, 'comments': comments, 'topics': topics}
    return render(request, 'place/profile.html', context)


@login_required(login_url='/login')
def createplace(request):
    form = PlaceForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)

        Places.objects.create(
            upload_by=request.user,
            topic=topic,
            name=request.POST.get('name'),
            located=request.POST.get('located'),
            hotel_name=request.POST.get('hotel_name'),
            description=request.POST.get('description')
        )
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'place/place_form.html', context)


@login_required(login_url='/login')
def updateplace(request, pk):
    place = Places.objects.get(id=pk)
    form = PlaceForm(instance=place)
    topics = Topic.objects.all()
    if request.user != place.upload_by:
        return HttpResponse('You Are Not Allow Here!!')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)

        place.topic = topic
        place.name = request.POST.get('name')
        place.located = request.POST.get('located')
        place.hotel_name = request.POST.get('hotel_name')
        place.description = request.POST.get('description')
        place.save()

        # form = PlaceForm(request.POST, instance=place)
        # if form.is_valid():
        # form.save()

        return redirect('home')
    context = {'place': place, 'form': form, 'topics': topics}
    return render(request, 'place/place_form.html', context)


@login_required(login_url='/login')
def deleteplace(request, pk):
    listplace = Places.objects.get(id=pk)
    if request.method == "POST":
        listplace.delete()
        return redirect('home')
    context = {'obj': listplace}
    return render(request, 'place/place_delete.html', context)


@login_required(login_url='/login')
def deletecomment(request, pk):
    comment = Message.objects.get(id=pk)
    if comment.user != comment.user:
        return HttpResponse("You are not Allow Here")
    if request.method == "POST":
        comment.delete()
        return redirect('home')
    context = {'obj': comment}
    return render(request, 'place/place_delete.html', context)


@login_required(login_url='/login')
def updateuser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
    if form.is_valid():
        form.save()
        return redirect('user-profile', pk=user.id)
    context = {'form': form}
    return render(request, 'place/update-user.html', context)


def topicpage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'place/mobile_topics.html', {'topics': topics})


def activitypage(request):
    comments = Message.objects.all()
    return render(request, 'place/mobile_activity.html', {'comments': comments})
