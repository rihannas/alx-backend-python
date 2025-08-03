# views.py

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect

@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    print('User deleted')
    return redirect('goodbye')  # Replace with your homepage or goodbye page
