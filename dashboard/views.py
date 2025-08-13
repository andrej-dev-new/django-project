from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard_view(request):
    user = request.user
    context = {
        'my_events': user.events.select_related('category').all(),
        'my_tickets': user.tickets.select_related('event').all(),
        'my_reviews': user.reviews.select_related('event').all(),
        'my_favorites': user.favorites.select_related('event').all(),
    }
    return render(request, 'dashboard/dashboard.html', context)
