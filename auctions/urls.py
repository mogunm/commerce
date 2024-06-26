from django.urls import path
from django.conf import settings
from django.conf.urls.static import static  
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path('listing/<int:listing_id>', views.listing, name="listing"),
    path('displayCategory', views.displayCategory, name="displayCat"),
    path("removeWatchlist/<int:listing_id>", views.removeWatchlist, name="removeWatchlist"),
    path("addWatchlist/<int:listing_id>", views.addWatchlist, name="addWatchlist"),
    path("displayWatchlist", views.displayWatchlist, name="displayWatchlist") ,
    path("addComment/<int:listing_id>", views.addComment, name="addComment"),
    path("addBid/<int:listing_id>", views.addBid, name="addBid"),
    path("removeListing/<int:listing_id>", views.removeListing, name="removeListing")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
