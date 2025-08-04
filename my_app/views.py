from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect,get_object_or_404
from my_app.forms import UserRegisterForm, ProfileForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from .models import BlogPost,Comment
from .forms import CommentForm,BlogPostForm
from django.urls import reverse



# Create your views here.

def register_view(request):
    if request.method=='POST':
        user_form=UserRegisterForm(request.POST)
        profile_form=ProfileForm(request.POST,request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()
            return redirect('login')
    else:
        user_form=UserRegisterForm()
        profile_form=ProfileForm()
    return render(request,'register.html',{'user_form':user_form,'profile_form':profile_form})

def login_view(request):
    if request.method=='POST':
       username=request.POST['username']
       password=request.POST['password']
       user=authenticate(request,username=username,password=password)
       if user is not None:
           print("Login successful!")
           login(request,user)
           return redirect('dashboard')
       else:
           print("Login failed: Invalid credentials.")
           return render(request,'login.html',{'error':'Invalid Credentials'})
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def custom_password_reset_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = f"http://127.0.0.1:8000/reset/{uid}/{token}/"

            subject = "Password Reset Request"
            message = render_to_string("password_reset_email.html", {
                "user": user,
                "reset_link": reset_link
            })

            send_mail(subject, message, "noreply@example.com", [email])
            messages.success(request, "Password reset email sent!")
            return redirect("password_complete")
        except User.DoesNotExist:
            messages.error(request, "No user with that email.")
    return render(request, "password_reset_form.html")

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Your password has been reset successfully.')
            return redirect('login')
        return render(request, 'password_reset_confirm.html', {'validlink': True})
    else:
        return render(request, 'password_reset_confirm.html', {'validlink': False})


def password_reset_done(request):
    return render(request, "password_reset_done.html")

def home_view(request):
    return render(request,'home.html')

@login_required
def dashboard_view(request):
    query = request.GET.get('q')
    if query:
        posts = BlogPost.objects.filter(title__icontains=query)
    else:
        posts = BlogPost.objects.all()

    paginator = Paginator(posts.order_by('-created_at'), 5)  # show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method=='POST':
        post_id=request.POST.get('post_id')
        post=get_object_or_404(BlogPost,id=post_id)
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.author=request.user
            comment.save()
            return redirect(f"{request.path}?page={page_number}#comments-{post_id}")

    comment_forms={post.id:CommentForm() for post in page_obj}

    editing_comment_id=request.GET.get('edit_comment_id')
    context={
        'posts':page_obj,
        'comment_forms':comment_forms,
        'editing_comment_id':int(editing_comment_id) if editing_comment_id else None,
    }

    return render(request, 'dashboard.html',context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('dashboard')  # Change if you have another redirect
    else:
        form = BlogPostForm()
    return render(request, 'create_post.html', {'form': form})
#
# @login_required
# def post_detail(request, post_id):
#     post = get_object_or_404(BlogPost, id=post_id)
#     comments = post.comments.all().order_by('-created_at')
#
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.author = request.user
#             comment.save()
#             return redirect('post_detail', post_id=post.id)
#     else:
#         form = CommentForm()
#
#     return render(request, 'post_detail.html',
#                   {'post': post, 'comments': comments, 'form': form})


def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    if request.user != post.author:
        return redirect('dashboard')  # or show a 403 page

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('dashboard')

    return render(request, 'edit_post.html', {'post': post})


def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    if request.user == post.author:
        post.delete()

    return redirect('dashboard')


def add_comment(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        post = BlogPost.objects.get(id=post_id)
        Comment.objects.create(post=post,
                               author=request.user,
                               content=content)
        return redirect(f"{reverse('post_detail',args=[post.id])}#comments")

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment.content=content
            comment.save()
        return redirect('dashboard')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    post_id = comment.post.id
    if comment.author==request.user:
       comment.delete()

    return redirect('dashboard')

