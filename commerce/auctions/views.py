from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
#from django.db.models import Max

from .models import User, Listing, Comments, Bids, Category
from .forms import NewListingForm, CommentsForm, PlaceBidForm


def index(request):
    """Index side, show all aktive listings"""
    user = request.user
    items = Listing.objects.all()

    if request.method == "POST":
        key = request.POST["item_id"]
        current = Listing.objects.get(pk=key)
    # the user is alredy watching when klicking then remove the user form the watchlist
        if current.is_watching(user):
            current.remove_from_watchlist(user)
        else:
        # User is not watching, add user to the watchlist
            current.add_to_watchlist(user)
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "auctions/index.html", {
        "items": items,
    })


def login_view(request):
    """login"""
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
    """logout"""
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """regester new user"""
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
    

def listing(request, pk):
    """see al detalies of each listing"""
    item = Listing.objects.get(pk=pk)
    user = request.user
    message = None

    if request.method == "POST":
        # Handling the comments
        if "comment_form" in request.POST:
            # Get users input aka the comment
            new_comment = CommentsForm(request.POST)
            # Saving the comment with the user and item id's 
            if new_comment.is_valid():
                new_comment.instance.user = user
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
        
        if "bid_form" in request.POST:
            # Get users input aka the bid
            offer = float(request.POST["bid"])
            if valid_bid(offer, item):
                item.current_bid = offer
                item.buyer = user
                form = PlaceBidForm(request.POST)
                new_bid = form.save(commit=False)
                new_bid.user = user
                new_bid.item = item
                new_bid.save()
                item.save()
                message = "Succes your bid:"
            else:
                message = "Your bid has to be more than: "
        
    context = {
        "message": message,
        "item": item,
        "new_comment": CommentsForm(),
        "new_bid": PlaceBidForm(),
        "watching": item.is_watching(user),
        "comments": item.item_comment.all(),
        "total_bids": Bids.total_bids(item.id)
    }
    # Handling page view, and adds item informatin, comments, and the watching button
    return render(request, "auctions/listing.html", context)


def valid_bid(offer, item):
    if offer >= item.starting_price and (item.current_bid is None or offer > item.current_bid):
        return True
    else: 
        return False


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all(),
        "items": Listing.objects.all()
    })


@login_required
def watchlist(request):
    """View alle items the user have on their watchlist"""
    if request.method == "POST":
        item = Listing.objects.get(pk=request.POST["item_id"])
        user = request.user
        # the user is watching an item showed on the watchlist if kickted remove from list
        item.remove_from_watchlist(user)
        return HttpResponseRedirect(reverse("watchlist"))

    return render(request, "auctions/watchlist.html", {
    "items": Listing.objects.filter(watch=request.user),
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

@login_required
def close(request, pk):
    """ User who is seller of listing can close the auction"""
    message = None
    item = Listing.objects.get(pk=pk)
    user = request.user

    if request.method == "POST":
        if item.seller == user:
            item.is_active = False
            item.save()
            message = "Congratulations your listing is closed"
        else: 
            message = "Unauthorized usage"

    
    return render(request, "auctions/close.html", {
        "item": item,
        "total_bids": Bids.total_bids(item.id),
        "message": message,

    })

@login_required
def myacutions(request):
    return render(request, "auctions/myauction.html", {
        "items": Listing.objects.all()
    })