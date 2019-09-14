from django.contrib import admin
from event.models import Event , Comment ,Category,Clap,View
# Register your models here.

admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(View)
admin.site.register(Clap)
