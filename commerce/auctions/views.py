from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listings, Comments, Bids , CAT_CHOICES, Watchlist

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = [
            "title",
            "author",
            "description",
            "price",
            'category',
            "image",
        ]

class CommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=200)
    class Meta:
        model = Comments
        fields = (
            "comment",
        )
    

class BidForm(forms.ModelForm):
    #bid = forms.DecimalField(max_value=100, decimal_places=2)
    class Meta:
        model = Bids
        fields = (
            'price',
            )

def index(request):
    return render(request, "auctions/index.html", {
       # "listings": Listings.objects.all().order_by("?")
       "listings": Listings.objects.filter(closed=False).order_by("?")
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
def create(request):
    user = User.objects.get(username=request.user)
    form = ListingForm(request.POST,request.FILES)
    if request.method == "POST" and form.is_valid:
        #if request.method == "POST":
        
        listing = form.save(commit=False)   
        listing.lister = user
        listing.save()

        return HttpResponseRedirect(reverse("index"))
    else: 
        form = ListingForm()
        return render(request, "auctions/create.html",{
            "form": form,
            "user": user
        })

@login_required
def watchlist(request):
    #must be signed in
    user = User.objects.get(username=request.user)
    return render(request, "auctions/watchlist.html",{
        "watchlist": user.watchlist.all()
    })

def categories(request):
        return render(request, "auctions/categories.html",{
            "categories": sorted(CAT_CHOICES)
        })
    

def listing(request, listing_id):
    listing = Listings.objects.get(id =listing_id)
    # bid form
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        if request.POST.get("button") == "watchlist":
            if not user.watchlist.filter(listing=listing):
                watchlist = Watchlist()
                watchlist.user = user
                watchlist.listing = listing
                watchlist.save()
            else:
                user.watchlist.filter(listing=listing).delete()
            return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
        if not listing.closed:
            if request.POST.get("button") == "close":
                listing.closed = True
                listing.save()
            else:
                price = float(request.POST["price"])
                #bids = listing.bids.all()
                if price <= listing.price:
                    return render(request, "auctions/listing.html",{
                        "listing": listing,
                        "message": "Bid must be higher than current price",
                        "form":BidForm(),
                        
                    })
                form = BidForm(request.POST or None)
                if form.is_valid():
                    #bid = form.save()
                    #bid.user = user
                    #bid.save()
                    #listing.bids.add(bid)
                    listing.price = price
                    listing.save()
                    return render(request, "auctions/listing.html",{
                        "listing":listing,
                        "form": form,
                        "commentForm": CommentForm(),
                
                    })
       
    return render(request, "auctions/listing.html",{
        "listing":listing,
        "form": BidForm(),
        "commentForm": CommentForm(),
       
    })

def item(request, categ):
    listings = Listings.objects.filter(category=categ).order_by('title')
    return render(request, "auctions/item.html",{
        "listings": listings,
    })

@login_required
def add_comment(request, listing_id):
    user = User.objects.get(username=request.user)
    listing = Listings.objects.get(id = listing_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.save()
            listing.comments.add(comment)
            listing.save()
            return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
        else: 
            return render(request, "auctions/comment.html",{
                "listing_id":listing.id,
                "form": form, 
            })
    else:
        return render(request, "auctions/comment.html",{
            "form": CommentForm(),
            "listing_id": listing.id
        })