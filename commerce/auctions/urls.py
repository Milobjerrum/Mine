from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:pk>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create", views.create, name="create"),
    path("close/<int:pk>", views.close, name="close"),
    path("myauctions", views.myacutions, name="myauctions")
]
