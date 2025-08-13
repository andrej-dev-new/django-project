from django.contrib import admin
from .models import Category, Event, Ticket, Review, Favorite

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'owner', 'starts_at', 'capacity', 'tickets_count')
    list_filter = ('category', 'starts_at')
    search_fields = ('title', 'description', 'location')
    ordering = ('starts_at',)
    date_hierarchy = 'starts_at'
    readonly_fields = ('created_at', 'slug')

    @admin.action(description="Approve selected events")
    def approve_events(self, request, queryset):
        self.message_user(request, f"Approved {queryset.count()} event(s).")

    actions = ['approve_events']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'seat_type', 'booked_at')
    list_filter = ('seat_type', 'booked_at')
    search_fields = ('user__username', 'event__title')
    ordering = ('-booked_at',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('event__title', 'user__username', 'comment')
    ordering = ('-created_at',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'created_at')
    search_fields = ('user__username', 'event__title')
    ordering = ('-created_at',)
