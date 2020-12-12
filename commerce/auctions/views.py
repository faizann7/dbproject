from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Listings, User, Comments, Bids
import datetime



def index(request):
    all_listings= Listings.objects.all()
    return render(request, "auctions/index.html",
    {
    "all_listings": all_listings, "message":"Active Listings"
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

def listing(request):
    if request.method=="POST":
        listing=Listings()
        listing.created_by=request.user
        listing.title=request.POST["title"]
        listing.description=request.POST["description"]
        listing.date=datetime.datetime.now()
        listing.starting_bid=request.POST["bid"]
        listing.Categories=request.POST["optradio"]
        listing.image=request.FILES["image"]
        listing.username=request.user
        listing.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/listing.html")

def item(request,item):
    comments=[]
    all_comments=Comments.objects.all()
    for comment in all_comments:
        if comment.item_id==item:
            comments.append(comment)

    listing=Listings.objects.get(id=item)

    if str(listing.created_by) == str(request.user):
        button=True
    else:
        button=False

    bids=[]
    all_bids=Bids.objects.all()
    for bid in all_bids:
        if bid.item_id == item:
            bids.append(bid.bid)

    if len(bids) > 1:
        highest_bid=max(bids)
    elif not bids:
        highest_bid=Listings.objects.get(id=item).starting_bid
    else:
        highest_bid,=bids

    winner=False
    if listing.highest_bidder==request.user.username:
        winner=True



    return render(request, "auctions/item.html",{
    "item":listing,"comments":comments, "highest_bid":highest_bid, "button":button,
    "winner":winner,
    })

def view_watchlist(request):
    listings=[]
    all_listings=Listings.objects.all()
    for list in all_listings:
        if list.watchlist == True:
            listings.append(list)

    return render(request, "auctions/random.html",{
    "watchlist": listings
    })

def change_watchlist(request, item):
    listing=Listings.objects.get(id=item)
    if listing.watchlist != True:
        listing.watchlist = True
    else:
        listing.watchlist=False
    listing.save()
    return render(request, "auctions/item.html",{
      "item":listing
        })

def categories(request):
    categories=[]
    listings=Listings.objects.all()
    for list in listings:
        if not list.Categories in categories:
            categories.append(list.Categories)
    return render(request, "auctions/categories.html",{
    "categories":categories
    })

def category_items(request,category):
    items=[]
    listings=Listings.objects.all()
    for list in listings:
        if category == list.Categories:
            items.append(list)
    return render(request, "auctions/index.html",{
    "all_listings":items, "message":category
    })

def comment(request, item):
    if request.method=="POST":
        new_comment=Comments()
        new_comment.comment=request.POST["comment"]
        new_comment.user=request.user
        new_comment.item_id=item
        new_comment.save()
    comments=[]
    all_comments=Comments.objects.all()
    for comment in all_comments:
        if comment.item_id==item:
            comments.append(comment)

    listing=Listings.objects.get(id=item)
    if str(listing.created_by) == str(request.user):
        button=True
    else:
        button=False


    bids=[]
    all_bids=Bids.objects.all()
    for bid in all_bids:
        if bid.item_id == item:
            bids.append(bid.bid)
    if not bids:
        highest_bid=Listings.objects.get(id=item).starting_bid
    elif len(bids) > 1:
        highest_bid=max(bids)
    else:
        highest_bid,=bids


    return render(request, "auctions/item.html",{
    "comments": comments, "item":listing, "highest_bid":highest_bid, "button":button,

    })

def placebid(request, item):
    bids=[]
    listing=Listings.objects.get(id=item)
    all_bids=Bids.objects.all()
    for bid in all_bids:
        if bid.item_id == item:
            bids.append(bid.bid)

    if not bids:
        highest_bid=Listings.objects.get(id=item).starting_bid
    elif len(bids)>1:
        highest_bid=max(bids)
    else:
        highest_bid,=bids
    if request.method=="POST":
        if int(request.POST["bid"])<Listings.objects.get(id=item).starting_bid and  not bids or bids and int(request.POST["bid"])<=highest_bid:
            return render(request, "auctions/error.html",{
                 "message": "Error: Bid should be larger than the current price"
                     })

        else:
            new_bid=Bids()
            new_bid.bid=request.POST["bid"]
            new_bid.user=request.user.username
            new_bid.item_id=item
            new_bid.save()
            highest_bid=new_bid.bid
            listing.highest_bidder=request.user.username
            listing.save()

    comments=[]
    all_comments=Comments.objects.all()
    for comment in all_comments:
        if comment.item_id==item:
            comments.append(comment)


    return render(request, "auctions/item.html",{
    "comments": comments, "item":listing, "highest_bid":highest_bid
    })

def close_bid(request,item):
    listing=Listings.objects.get(id=item)
    listing.close_bid=True
    listing.save()

    comments=[]
    all_comments=Comments.objects.all()
    for comment in all_comments:
        if comment.item_id==item:
            comments.append(comment)
    return render(request, "auctions/item.html",{
    "item":listing,"comments":comments

    })
