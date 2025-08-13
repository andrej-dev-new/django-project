from django.urls import path
from .views import (
    EventListView, EventDetailView,
    EventCreateView, EventUpdateView, EventDeleteView,
    TicketCreateView,
    ReviewCreateView, ReviewUpdateView, ReviewDeleteView,
    favorite_add, favorite_remove, FavoriteListView
)

app_name = 'events'

urlpatterns = [
    path('', EventListView.as_view(), name='list'),
    path('favorites/', FavoriteListView.as_view(), name='favorites'),
    path('create/', EventCreateView.as_view(), name='create'),
    path('<slug:slug>/', EventDetailView.as_view(), name='detail'),
    path('<slug:slug>/edit/', EventUpdateView.as_view(), name='edit'),
    path('<slug:slug>/delete/', EventDeleteView.as_view(), name='delete'),

    path('<slug:slug>/ticket/', TicketCreateView.as_view(), name='ticket_create'),

    path('<slug:slug>/review/', ReviewCreateView.as_view(), name='review_create'),
    path('review/<int:review_id>/edit/', ReviewUpdateView.as_view(), name='review_edit'),
    path('review/<int:review_id>/delete/', ReviewDeleteView.as_view(), name='review_delete'),

    path('<slug:slug>/favorite/add/', favorite_add, name='favorite_add'),
    path('<slug:slug>/favorite/remove/', favorite_remove, name='favorite_remove'),
]
