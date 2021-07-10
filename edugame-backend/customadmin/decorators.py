from functools import wraps
from django.contrib.auth import logout
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import resolve_url
from urllib.parse import urlparse
from edugame.settings import ADMINUSER_LOGIN_URL

def admin_user_login_required(view_func, function=None, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    @wraps(view_func)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        logout(request)

        path = request.build_absolute_uri()
        resolved_login_url = resolve_url(ADMINUSER_LOGIN_URL)
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (not login_scheme or login_scheme == current_scheme) and (
                not login_netloc or login_netloc == current_netloc
        ):
            path = request.get_full_path()
        from django.contrib.auth.views import redirect_to_login

        return redirect_to_login(path, resolved_login_url, redirect_field_name)

    return wrap
