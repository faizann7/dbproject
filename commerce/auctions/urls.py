from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('listing', views.listing, name="listing"),
    path("listing/<int:item>",views.item, name="item"),
    path("view_watchlist",views.view_watchlist, name="view_watchlist"),
    path("change_watchlist/<int:item>", views.change_watchlist, name="change_watchlist"),
    path("categories", views.categories, name="categories"),
    path("category_items/<str:category>", views.category_items, name="category_items"),
    path("comment/<int:item>", views.comment, name="comment"),
    path("placebid/<int:item>", views.placebid, name="placebid"),
    path("close_bid/<int:item>", views.close_bid, name="close_bid")

]
