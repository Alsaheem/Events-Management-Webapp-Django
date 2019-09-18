from django.shortcuts import render,get_object_or_404,redirect
from event.models import Event , Comment
from django.views.generic.edit import FormMixin
from django.utils import timezone
from django.contrib import messages
from event.forms import EventForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView,View )
from actions.utils import create_action
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
class Homepage(TemplateView):
    template_name = 'home.html'

class EventListView(ListView,LoginRequiredMixin):
    context_object_name = 'events'
    template_name = 'event/event_list.html'
    model = Event
    ordering = ['-published_date']
    # paginate_by = 4   

class EventDisplay( DetailView):
    model = Event
    template_name = 'event/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.get_object().comments.all()
        context['attending'] = self.get_object().attendees.all
        return context


class CommentCreate(SuccessMessageMixin,CreateView):
    model = Comment
    template_name = 'event/event_detai.html'
    fields = ('comment_text',)
    success_message = 'Comment was added successfully'

    def form_valid(self, form):
        form.instance = form.save(commit=False)
        form.instance.event = self.get_object(queryset=Event.objects.all())
        form.instance.author = self.request.user
        create_action(self.request.user, 'added a comment', form.instance)
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('events:event_detail', kwargs={'pk': self.get_object(Event.objects.all()).pk})

class EventDetailView(View,LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        view = EventDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentCreate.as_view()
        return view(request, *args, **kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(Event,self.get_object(Event.objects.all()).pk)
        context['user_can_clap'] = event.user_can_clap(self.request.user)
        return context

    def get_object(self,**kwargs):
        event_pk = self.kwargs.get('pk')
        event_query = Event.objects.filter(pk=event_pk)
        if event_query.exists():
            event_object  = event_query.first()
            view , created = View.objects.get_or_create(
                user = self.request.user ,
                event = event_object
            )
            if view:
                event.views += 1
                view.save()
            return event_object
        else:
            return event_object



class EventFormMixin(object):
    def form_valid(self, form):
        form.instance.creator = self.request.user
        create_action(self.request.user, 'created a new event', form.instance)
        return super().form_valid(form)


class EventCreateView(LoginRequiredMixin, SuccessMessageMixin, EventFormMixin, CreateView):
    model = Event
    template_name = 'event/event_create_form.html'
    form_class = EventForm
    context_object_name = 'event'
    success_message = "%(title)s was created successfully"

class EventUpdateView(LoginRequiredMixin, SuccessMessageMixin, EventFormMixin, UpdateView):
    model = Event
    template_name = 'event/update_form.html'
    template_name_suffix = '_update_form'
    form_class = EventForm
    success_message = "%(title)s was updated successfully"


class EventDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Event
    template_name = 'events/event_delete.html'
    success_url = reverse_lazy('events:event_list')
    context_object_name = 'event'
    success_message = "%(title)s was deleted successfully"

@login_required()
def attend_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    # attendee = User.objects.get(username=request.user)
    attendee = request.user
    event.attendees.add(attendee)
    create_action(attendee, 'is attending', event)
    messages.success(request, 'You are now attending {0}'.format(event.title))
    return redirect('events:event_detail', pk=event.pk)


@login_required()
def not_attend_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    attendee = request.user
    event.attendees.remove(attendee)
    create_action(attendee, 'no longer attending', event)
    messages.success(request, 'You are no longer attending {0}'.format(event.title))
    return redirect('events:event_detail', pk=event.pk)


@login_required()
def clap(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if not event.user_can_clap(request.user):
        messages.error(request,'No Choice was selected')
        return redirect('events:event_detail', pk=event.pk)
    else:
        event.claps += 1
        return redirect('events:event_detail', pk=event.pk)
