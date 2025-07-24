from django.shortcuts import render,redirect
from .mongosetup import client
from django.contrib.auth.hashers import make_password,check_password
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        db = client['sdp3']
        users_collection = db['users']
        user = users_collection.find_one({
            '$or': [
                {'username': username_or_email},
                {'email': username_or_email}
            ]
        })
        if user and check_password(password, user['password']):
            # Optionally, set session here
            return redirect(reverse('index'))
        else:
            return render(request, 'login.html', {'error': 'Invalid username/email or password.'})
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match.'})

        db = client['sdp3']
        users_collection = db['users']

        # Check for existing user
        if users_collection.find_one({'$or': [{'username': username}, {'email': email}]}):
            return render(request, 'signup.html', {'error': 'Username or email already exists.'})

        # Insert new user
        users_collection.insert_one({
            'username': username,
            'email': email,
            'password': make_password(password)
        })
        return redirect('login')
    return render(request, 'signup.html')

def dashboard():
