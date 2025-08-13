from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import EventForm, TicketForm, ReviewForm
from .mixins import OwnerRequiredMixin
from .models import Event, Ticket, Review, Favorite, Category

# PUBLIC VIEWS
class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):
        qs = Event.objects.select_related('category', 'owner').order_by('starts_at')
        category_slug = self.request.GET.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        event = self.object
        ctx['ticket_form'] = TicketForm()
        ctx['review_form'] = ReviewForm()
        if self.request.user.is_authenticated:
            ctx['has_ticket'] = Ticket.objects.filter(user=self.request.user, event=event).exists()
            ctx['is_favorite'] = Favorite.objects.filter(user=self.request.user, event=event).exists()
            ctx['my_review'] = Review.objects.filter(user=self.request.user, event=event).first()
        return ctx

# PRIVATE VIEWS (CRUD)
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Event created successfully.")
        return super().form_valid(form)

class EventUpdateView(OwnerRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        messages.success(self.request, "Event updated successfully.")
        return super().form_valid(form)

class EventDeleteView(OwnerRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('events:list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Event deleted.")
        return super().delete(request, *args, **kwargs)

# Tickets
class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'events/ticket_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, slug=kwargs['slug'])
        if self.event.tickets_count >= self.event.capacity:
            messages.error(request, "This event is sold out.")
            return redirect(self.event.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.event = self.event
        try:
            response = super().form_valid(form)
        except Exception:
            messages.error(self.request, "You already have a ticket for this event.")
            return redirect(self.event.get_absolute_url())
        messages.success(self.request, "Ticket booked. See you there!")
        return response

    def get_success_url(self):
        return self.event.get_absolute_url()

# Reviews
class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'events/review_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, slug=kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.event = self.event
        try:
            response = super().form_valid(form)
        except Exception:
            messages.error(self.request, "You already reviewed this event.")
            return redirect(self.event.get_absolute_url())
        messages.success(self.request, "Thanks for your review!")
        return response

    def get_success_url(self):
        return self.event.get_absolute_url()

class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'events/review_form.html'
    pk_url_kwarg = 'review_id'

    def dispatch(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user and not request.user.is_staff:
            return HttpResponseForbidden("Not allowed.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.event.get_absolute_url()

class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'events/event_confirm_delete.html'
    pk_url_kwarg = 'review_id'

    def dispatch(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user and not request.user.is_staff:
            return HttpResponseForbidden("Not allowed.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.event.get_absolute_url()

# Favorites (extra funkciq za bonus tocki)
@login_required
def favorite_add(request, slug):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    event = get_object_or_404(Event, slug=slug)
    Favorite.objects.get_or_create(user=request.user, event=event)
    messages.success(request, "Added to favorites.")
    return redirect(event.get_absolute_url())

@login_required
def favorite_remove(request, slug):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    event = get_object_or_404(Event, slug=slug)
    Favorite.objects.filter(user=request.user, event=event).delete()
    messages.info(request, "Removed from favorites.")
    return redirect(event.get_absolute_url())

class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'events/favorites.html'
    context_object_name = 'favorites'
    paginate_by = 10

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('event')

# Error handlers
def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)
