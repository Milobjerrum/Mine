from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Listing, Comments
from .forms import NewListingForm, CommentsForm


def index(request):
    return render(request, "auctions/index.html", {
        "items": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    

@login_required
def listing(request, pk):
    """see al detalies of each listing"""

    if request.method == "POST":
        new_comment = CommentsForm(request.POST)
        # adding the users comment, and saving user and item id to it. 
        if new_comment.is_valid():
            new_comment.instance.user = request.user
            new_comment.instance.item_id = pk
            new_comment.save()
            return HttpResponseRedirect(reverse("listing", args=[str(pk)]))
        

    watch_item = get_object_or_404(Listing, id=pk)
    is_watching = False
    if watch_item.watch.filter(id=request.user.id).exists():
        is_watching = True

    return render(request, "auctions/listing.html", {
        "item": Listing.objects.get(pk=pk),
        "comments": Comments.objects.filter(item_id=pk),
        "new_comment": CommentsForm(),
        "is_watching": is_watching
    })

def watch(request, pk):
    """ Tracking if a user is watching a item"""
    item = get_object_or_404(Listing, id=request.POST.get("item_id"))

    is_watching = False
    if item.watch.filter(id=request.user.id).exists():
        item.watch.remove(request.user)
        is_watching = False

    else:
        item.watch.add(request.user)
        is_watching = True

    return HttpResponseRedirect(reverse("listing", args=[str(pk)]))



@login_required
def categories(request):
    return render(request, "auctions/categories.html")


@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
    "items": Listing.objects.filter(watch=request.user)
    })

@login_required
def create(request):
    """User can create a new listing"""
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            form.instance.seller = request.user
            form.save()
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create.html", {
        "form": NewListingForm()
    })
