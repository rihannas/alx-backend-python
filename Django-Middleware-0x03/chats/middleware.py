import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden


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
