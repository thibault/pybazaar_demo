from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from annoying.decorators import render_to


@render_to('accounts/login.html')
def login(request):
    users = User.objects.all()

    if request.method == 'POST':
        username = request.POST.get('user', None)
        user = authenticate(username=username, password='pass')
        auth_login(request, user)

    return {
        'users': users
    }
