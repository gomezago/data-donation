from django.shortcuts import render
from about.models import Post, Comment
from .forms import CommentForm

# Create your views here.
def about_index(request): #Display list of posts
    posts = Post.objects.all().order_by('-created_on')
    context = {
        "posts": posts,
    }
    return render(request, "about_index.html", context)

def about_category(request, category): #Category as argument for the query
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-created_on'
    )
    context = {
        "category": category,
        "posts": posts
    }
    return render(request, "about_category.html", context)

def about_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
    }

    return render(request, "about_detail.html", context)

def about_detail(request, pk): # Check if request was sent to the server
    post = Post.objects.get(pk=pk)

    form = CommentForm()
    if request.method == 'POST': # Check if POST request has been received
        form = CommentForm(request.POST)
        if form.is_valid(): # Check that posts have been entered correctly
            #TODO: IF form is invalid, display errors
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post
            )
            comment.save() # Save comment

    comments = Comment.objects.filter(post=post) # Query DB and add the form to dictionary
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request, "about_detail.html", context)