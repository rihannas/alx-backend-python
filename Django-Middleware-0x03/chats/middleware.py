import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden
from django.http import JsonResponse


logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('user_requests.log')
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define allowed access hours (from 6:00 to 21:00)
        self.start_time = time(6, 0)   # 6:00 AM
        self.end_time = time(21, 0)    # 9:00 PM

    def __call__(self, request):
        now = datetime.now().time()

        # Check if current time is outside allowed hours
        # Allowed time: from 6:00 (inclusive) to 21:00 (inclusive)
        if not (self.start_time <= now <= self.end_time):
            return HttpResponseForbidden("Access to the messaging app is restricted between 9 PM and 6 AM.")

        # Otherwise allow request
        response = self.get_response(request)
        return response


import time as time_module

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store IP access info as {ip: [(timestamp1), (timestamp2), ...]}
        self.ip_message_times = {}
        self.limit = 5  # max messages
        self.window_seconds = 60  # 1 minute window

    def __call__(self, request):
        # Only count POST requests to the messaging endpoint
        if request.method == "POST" and request.path.startswith('/api/messages/'):
            ip = self.get_client_ip(request)
            now = time_module.time()
            times = self.ip_message_times.get(ip, [])

            # Remove timestamps older than window
            times = [t for t in times if now - t < self.window_seconds]

            if len(times) >= self.limit:
                return JsonResponse(
                    {"detail": "Rate limit exceeded: Max 5 messages per minute."},
                    status=429
                )

            # Add current timestamp and update dict
            times.append(now)
            self.ip_message_times[ip] = times

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        # Handle common proxy headers to get real IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply role checks to authenticated users
        user = getattr(request, 'user', None)

        if user and user.is_authenticated:
            # Example check: assume user model has a 'role' field
            user_role = getattr(user, 'role', None)
            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden("403 Forbidden: You do not have permission to perform this action.")

        return self.get_response(request)
