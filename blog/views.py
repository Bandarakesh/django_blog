from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import Post
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like
from .forms import CommentForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post
# User Registration View
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            print("User registered and logged in successfully:", user.username)
            return redirect('home')  # Redirect to home after successful registration
        else:
            print("Form errors:", form.errors)  # Log form errors for debugging
    else:
        form = UserRegistrationForm()  # Empty form when no POST data
    return render(request, 'blog/register.html', {'form': form})


# Home View with Post Filtering by School
def home(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(author__school=request.user.school)  # Filter posts based on user's school
        liked_posts = Like.objects.filter(user=request.user).values_list('post', flat=True)
    else:
        posts = Post.objects.none()  # No posts for unauthenticated users
        liked_posts = []
    return render(request, 'blog/home.html', {
        'posts': posts,
        'liked_posts': liked_posts  # Pass liked posts as a list of post IDs
    })

# Login View
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home after successful login
    else:
        form = AuthenticationForm()  # Empty form when no POST data
    return render(request, 'blog/login.html', {'form': form})

# Logout View
def user_logout(request):
    logout(request)
    return redirect('home')  # Redirect to home after logging out

@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    
    # Check if the user has already liked the post
    if not Like.objects.filter(post=post, user=user).exists():
        Like.objects.create(post=post, user=user)
    return redirect('home')  # Redirect to the home page after liking the post

# Comment on a post
@login_required
def comment_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('home')


@login_required  # Ensures only logged-in users can create posts
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Associate the post with the current user
            post.save()
            return redirect('home')  # Redirect to home after saving the post
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})
