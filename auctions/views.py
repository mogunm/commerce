from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Category, Comment, Bid


def index(request):
    # get all the active listings data from the database
    activeListings = Listing.objects.filter(is_active=True)
    allCategories = Category.objects.all()

    return render(request, "auctions/index.html", {
        "listings": activeListings,
        "categories":  allCategories
    })

def addBid(request, listing_id):
    newBid = request.Post['bid']
    listing = Listing.objects.get(id=listing_id)

    # checks the user agasint the poster of the listing 
    isUser = request.user.username == listing.user.username

    # see if user is in the watchlist for the listing
    inWatchlist = request.user in listing.watchlist.all()

    # get all of the comments from tne database 
    comments = Comment.objects.filter(listing=listing_id)

    if newBid > listing.price.bid:
        # update the new bid and save it to the database 
        updateBid = Bid(bid=float(newBid), user=request.user)
        updateBid.save()

        # update the price of the bid on the listing to the highest bid 
        listing.price = updateBid
        listing.save()


        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Bid was updated succesfully!",
            "update": True,
            "inWatchlist": inWatchlist,
            "comments": comments,
            "isUser": isUser

        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Bid was not updated succesfully!",
            "update": False,
            "inWatchlist": inWatchlist,
            "comments": comments,
            "isUser": isUser

        })


def addComment(request, listing_id):
    # get user 
    user = request.user

    # get the listing the data from database 
    listing = Listing.objects.get(id=listing_id)

    # get comment from the form 
    comment = request.POST['comment']

    # create the comment object
    newComment = Comment(
        owner = user,
        listing = listing,
        message = comment
    )

    # save the comment in databse 
    newComment.save()

    return HttpResponseRedirect(reverse('listing', args=(listing_id, )))



def addWatchlist(request, listing_id):
    # grab listing data from database 
    listing = Listing.objects.get(id=listing_id)

    # get user 
    user = request.user 

    # add this user to the watchlist of the listing 
    listing.watchlist.add(user)

    # redirect to the listing page 
    return HttpResponseRedirect(reverse('listing', args=(listing_id, )))

def removeWatchlist(request, listing_id):
    # grab listing data from database 
    listing = Listing.objects.get(id=listing_id)

    # get user 
    user = request.user 

    # add this user to the watchlist of the listing 
    listing.watchlist.remove(user)

    # redirect to the listing page 
    return HttpResponseRedirect(reverse('listing', args=(listing_id, )))

def displayWatchlist(request):
    user = request.user 

    # get the watchlistings for user 
    listings = user.watchlist.all()


    return render(request, "auctions/watchlist.html", {
        "watchlistings":  listings
    })


def create(request):
     # get all of the categories
    allCategories = Category.objects.all()

    if request.method == "POST":

        # get all of the field values to send to tge database 
        title = request.POST["title"]
        description = request.POST['description']
        price = request.POST['price']
        category = request.POST['category']
        imageurl = request.FILES['image']

        # get current user 
        user = request.user

        # create bid instance for the listing table 
        bid = Bid(bid=float(price), user = user)
        bid.save()

        # get the category data 
        categoryData = Category.objects.get(category_name=category)

        # send values to the database 
        listing = Listing(
            title=title, 
            description=description, 
            price=bid, 
            category=categoryData, 
            image_url=imageurl, 
            user=user
            )

        # save the changes to database 
        listing.save()

        # redirect back to index 
        return HttpResponseRedirect(reverse("index"))

    # if the request method is GET 
    return render(request, "auctions/create.html", {
        "categories": allCategories
    })

def displayCategory(request):
    if request.method == "POST":
        # getting the category data from database 
        formCat = request.POST['category']
        category = Category.objects.get(category_name=formCat)

        # get filter listing and all categories to display on page
        liveListings = Listing.objects.filter(is_active=True, category=category)
        allCategories = Category.objects.all()

        return render(request, "auctions/index.html", {
            "listings": liveListings,
            "categories": allCategories
        })
    
def removeListing(request, listing_id):
    # get listing data from data base 
    listing = Listing.objects.get(id=listing_id)

    # checks the user agasint the poster of the listing 
    isUser = request.user.username == listing.user.username

    # see if user is in the watchlist for the listing
    inWatchlist = request.user in listing.watchlist.all()

    # get all of the comments from tne database 
    comments = Comment.objects.filter(listing=listing_id)

    listing.is_active = False
    listing.save()

    return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Congratulations, you have closed the auction!",
            "update": True,
            "inWatchlist": inWatchlist,
            "comments": comments,
            "isUser":isUser

        })

@login_required(login_url='login')
def listing(request, listing_id):
    # get listing data from database 
    listing = Listing.objects.get(id=listing_id)

    # see if user is in the watchlist for the listing
    inWatchlist = request.user in listing.watchlist.all()

    # get all of the comments from tne database 
    comments = Comment.objects.filter(listing=listing_id)

    # checks the user agasint the poster of the listing 
    isUser = request.user.username == listing.user.username

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "inWatchlist": inWatchlist,
        "comments": comments,
        "isUser": isUser
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
