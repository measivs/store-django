import datetime

from django.utils.timezone import now
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout
from django.shortcuts import redirect

class UpdateLastActiveMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            request.user.update_last_active()


class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.timeout = 60

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        last_activity = request.session.get('last_activity')

        if last_activity:
            elapsed_time = (now() - datetime.datetime.fromisoformat(last_activity)).total_seconds()
            if elapsed_time > self.timeout:
                logout(request)
                return redirect('login')

        request.session['last_activity'] = now().isoformat()
        return self.get_response(request)
