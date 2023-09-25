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
    item = Listing.objects.get(pk=pk)
    user = request.user


    if request.method == "POST":
        # Handling the comments
        if "comment_form" in request.POST:
            # Get users input aka the comment
            new_comment = CommentsForm(request.POST)
            # Saving the comment with the user and item id's 
            if new_comment.is_valid():
                new_comment.instance.user = request.user
                new_comment.instance.item_id = pk
                new_comment.save()
                return HttpResponseRedirect(reverse("listing", args=[str(pk)]))

        # Handeling the watch buttom
        if "watch_form" in request.POST:
            # the user is alredy watching when klicking then remove the user form the watchlist
            if item.is_watching(user):
                item.remove_from_watchlist(user)
            else:
                # User is not watching, add user to the watchlist
                item.add_to_watchlist(user)
            return HttpResponseRedirect(reverse("listing", args=[str(pk)]))

    # Handling page view, and adds item informatin, comments, and the watching button
    return render(request, "auctions/listing.html", {
        "item": item,
        "comments": Comments.objects.filter(item_id=pk),
        "new_comment": CommentsForm(),
        "watching": item.is_watching(user)
    })


@login_required
def categories(request):
    return render(request, "auctions/categories.html")


@login_required
def watchlist(request):
    """View alle items the user have on their watchlist"""
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
            new_listing = form.save()

            return HttpResponseRedirect(reverse("listing", args=[str(new_listing.pk)]))

    return render(request, "auctions/create.html", {
        "form": NewListingForm()
    })
