from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import Http404
from homepage.forms import ProfileForm


def index(request):
    template_name = 'homepage/index.html'
    #if request.user.is_authenticated():
    return render(request, template_name)


def profile(request):
    if not request.user.is_authenticated():
        raise Http404
    Group

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            message = "Profile Updated Successfully"
            message_type = "info"
        else:
            message = "There was a problem in saving user data"
            message_type = "danger"
    else:
        form = ProfileForm(instance=request.user)
        message = None
        message_type = None
    return render(request, 'homepage/profile.html', {'form': form, 'message': message, 'message_type': message_type})
