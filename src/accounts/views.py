from annoying.decorators import render_to


@render_to('accounts/login.html')
def login(request):
    return {}
