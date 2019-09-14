from django.urls import path,include
from event.views import Homepage,EventListView,EventDetailView,EventCreateView,EventDeleteView,EventUpdateView,attend_event,not_attend_event


app_name = 'events'

urlpatterns = [
    path('', Homepage.as_view() ,name='home'),
    path('events/', EventListView.as_view() ,name='event_list'),
    path('events/<int:pk>/',EventDetailView.as_view() , name='event_detail'),
    path('events/new/', EventCreateView.as_view(), name='event_create' ),
    path('events/<int:pk>/delete',EventDeleteView.as_view(), name='event_delete'),
    path('events/<int:pk>/update', EventUpdateView.as_view(), name='event_update'),
    path('events/<event_id>/attend/', attend_event, name='attend_event'),
    path('events/<event_id>/not_attend/', not_attend_event, name='not_attend_event')
]

