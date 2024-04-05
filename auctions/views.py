from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category


def index(request):
    # get the listings from the database
    listings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        "listings": listings
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
        currentUser = request.user

        # get the category data 
        categoryData = Category.objects.get(category_name=category)

        # send values to the database 
        listing = Listing(title=title, description=description, price=float(price), category=categoryData, image_url=imageurl, user=currentUser)

        # save the changes to database 
        listing.save()

        # redirect back to index 
        return HttpResponseRedirect(reverse("index"))

    # if the request method is GET 
    return render(request, "auctions/create.html", {
        "categories": allCategories
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
