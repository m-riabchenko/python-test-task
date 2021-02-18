from django.contrib.auth import login, get_user_model, logout, authenticate
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
import random
import string

from python_test_task.magic_auth.forms import EmailForm
from python_test_task.settings import HOST

User = get_user_model()


def enter_email(request):
    """
    Create new user with email and random token
    If user is exists token was updated
    """
    context = {}
    if request.method == "POST":
        form = EmailForm(data=request.POST)
        if form.is_valid():
            email = form.data["email"]
            token = ''.join(random.sample(string.ascii_lowercase, 6))
            user, _ = User.objects.get_or_create(email=email)
            user.token = token
            user.count_link = 0
            user.save()
            success = send_mail(
                subject='Magic link token',
                message='Click on ' + HOST + 'auth/' + token,
                from_email="mriabchenko11@gmail.com",
                recipient_list=[email],
                fail_silently=False,
            )
            if success:
                context["message"] = "Email was sent!"
            else:
                context["error"] = "Oops, Something went wrong!"

    if request.user.is_authenticated:
        context["msg"] = f"You already authenticated under this email {request.user.email}"

    return render(request, 'magic_auth/enter_email.html', context)


def auth(request, magic_token):
    user = get_object_or_404(User, token=magic_token)
    login(request, user)

    user.count_link += 1
    user.count_total += 1
    user.save()

    context = {"user": {
        "count_link": user.count_link,
        "count_total": user.count_total,
        "email": user.email
    }}

    return render(request, 'magic_auth/auth_user.html', context)

