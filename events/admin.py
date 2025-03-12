from django.contrib import admin
from .models import Event, EventRegistration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'current_participants', 'max_participants')
    list_filter = ('date', 'location')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('current_participants',)

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'registration_date', 'is_approved')
    list_filter = ('is_approved', 'registration_date', 'event')
    search_fields = ('user__username', 'event__title')
    date_hierarchy = 'registration_date'
