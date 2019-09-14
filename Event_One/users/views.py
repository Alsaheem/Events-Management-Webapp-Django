from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.forms import profileUpdateForm,userUpdateForm
from users.models import Profile
from event.models import Event
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render,get_object_or_404,redirect
# Create your views here.


@login_required
def Profile(request):
    # user = get_object_or_404(User,username=self.kwargs.get('username'))
    my_events = Event.objects.filter(creator=request.user).order_by('-created_date')
    if request.method== 'POST':
        u_form = userUpdateForm(request.POST,instance=request.user)
        p_form = profileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been successfully updated!')
            return redirect('users:profile')
    else:
        u_form = userUpdateForm(instance=request.user)
        p_form = profileUpdateForm(instance=request.user.profile)

    context= {
        'u_form':u_form,
        'p_form':p_form,
        'my_events':my_events
    }
    return render(request,'profile/profile.html',context)
