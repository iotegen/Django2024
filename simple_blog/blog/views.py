from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm,UpdateForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

    
@csrf_exempt
def post_list(request):
    posts = Post.objects.all()
    users = User.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Logged in as {username}")
            return redirect('post_list')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request,'post_list.html',{'posts':posts,'users':users})


def post_detail(request,post_id):
    post = get_object_or_404(Post,id=post_id) 
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post=post
            new_comment.author=comment_form.cleaned_data['user']
            new_comment.save()
            return redirect('post_detail',post_id=post.id)
    else:
        comment_form = CommentForm()    
    return render(request,'post_detail.html',{'post':post,'comments':comments,'comment_form':comment_form})


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.save()
            return redirect('post_detail',post_id=new_post.id)
        
    else:
        form = PostForm()
    return render(request,'post_form.html',{'form':form})


def post_edit(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    if request.method == 'POST':
        form = UpdateForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail',post_id=post.id)
    
    else:
        form = UpdateForm(instance=post)
    return render(request,'post_edit.html',{'form':form})


@csrf_exempt
def post_delete(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request,'post_form.html',{
        'post':post,
        'delete_mode':True
    })


def profile_redirect(request):
    username = request.GET.get('username')
    if username:
        return redirect('profile', username=username)
    return redirect('post_list')        
