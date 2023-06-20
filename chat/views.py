from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def chat_view(request):
    user_list = User.objects.all()  # Retrieve the list of users

    return render(request, 'chat/chat.html', {'user_list': user_list})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User is valid, login the user
            login(request, user)
            return redirect('chat')  # Redirect to the chat page after successful login
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'chat/login.html')
