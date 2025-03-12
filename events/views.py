from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.db.models import Count, Sum, Q
from django.utils import timezone
from .models import Event, EventRegistration
from .forms import EventForm, EventRegistrationForm, UserRegistrationForm
import logging

# Get logger for events app
logger = logging.getLogger('events')

def is_admin(user):
    return user.is_superuser

def event_list(request):
    events = Event.objects.all().order_by('date')
    logger.info(f"User {request.user} viewed event list")
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user.is_authenticated:
        registration = EventRegistration.objects.filter(event=event, user=request.user).first()
    else:
        registration = None
    logger.info(f"User {request.user} viewed event {event.title}")
    return render(request, 'events/event_detail.html', {
        'event': event,
        'registration': registration
    })

@user_passes_test(is_admin)
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            logger.info(f"Admin {request.user} created new event: {event.title}")
            messages.success(request, 'Event created successfully!')
            return redirect('event_detail', pk=event.pk)
        else:
            logger.error(f"Event creation failed by {request.user}. Errors: {form.errors}")
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Create Event'})

@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.is_full:
        logger.warning(f"User {request.user} attempted to register for full event: {event.title}")
        messages.error(request, 'Sorry, this event is full!')
        return redirect('event_detail', pk=pk)

    if request.method == 'POST':
        form = EventRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.user = request.user
            registration.save()
            logger.info(f"User {request.user} registered for event: {event.title}")
            messages.success(request, 'Registration submitted successfully! Awaiting approval.')
            return redirect('event_detail', pk=pk)
        else:
            logger.error(f"Registration failed for user {request.user}. Errors: {form.errors}")
    else:
        form = EventRegistrationForm()

    return render(request, 'events/event_registration.html', {
        'form': form,
        'event': event
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info(f"New user registered: {user.username}")
            messages.success(request, 'Registration successful!')
            return redirect('event_list')
        else:
            logger.error(f"User registration failed. Errors: {form.errors}")
    else:
        form = UserRegistrationForm()
    return render(request, 'events/register.html', {'form': form})

@user_passes_test(is_admin)
def manage_registrations(request):
    registrations = EventRegistration.objects.all().order_by('-registration_date')
    logger.info(f"Admin {request.user} accessed registration management")
    return render(request, 'events/manage_registrations.html', {'registrations': registrations})

@user_passes_test(is_admin)
def approve_registration(request, pk):
    registration = get_object_or_404(EventRegistration, pk=pk)
    registration.is_approved = True
    registration.save()
    registration.event.current_participants += 1
    registration.event.save()
    logger.info(f"Admin {request.user} approved registration for user {registration.user} for event {registration.event.title}")
    messages.success(request, 'Registration approved successfully!')
    return redirect('manage_registrations')

@user_passes_test(is_admin)
def dashboard(request):
    # Get total events and registrations
    total_events = Event.objects.count()
    total_registrations = EventRegistration.objects.count()
    approved_registrations = EventRegistration.objects.filter(is_approved=True).count()
    pending_registrations = EventRegistration.objects.filter(is_approved=False).count()

    # Get events with their registration counts
    events_with_registrations = Event.objects.annotate(
        registration_count=Count('eventregistration'),
        approved_count=Count('eventregistration', filter=Q(eventregistration__is_approved=True))
    ).order_by('-date')[:5]  # Get latest 5 events

    # Get registration statistics by date
    recent_registrations = EventRegistration.objects.filter(
        registration_date__gte=timezone.now() - timezone.timedelta(days=7)
    ).order_by('registration_date')

    logger.info(f"Admin {request.user} accessed dashboard")
    logger.debug(f"Dashboard stats - Events: {total_events}, Registrations: {total_registrations}, Approved: {approved_registrations}, Pending: {pending_registrations}")

    context = {
        'total_events': total_events,
        'total_registrations': total_registrations,
        'approved_registrations': approved_registrations,
        'pending_registrations': pending_registrations,
        'events_with_registrations': events_with_registrations,
        'recent_registrations': recent_registrations,
    }
    return render(request, 'events/dashboard.html', context)
