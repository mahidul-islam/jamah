from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Blog
from django.contrib import messages
from .forms import CreateBlogForm


def allblog(request):
    blogs = Blog.objects.all()
    context = {
        'blogs':blogs
    }
    template = loader.get_template('blog/allblog.html')
    return HttpResponse(template.render(context, request))

def create(request):
    if request.POST:
        form = CreateBlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit = False)
            blog.author = request.user
            blog.save()
            # messages.success(request, "is double message working")
            messages.add_message(request, messages.SUCCESS, 'Added new BLOG.')
            return HttpResponseRedirect(reverse('blog:allblog'))
    template = loader.get_template('blog/create.html')
    form = CreateBlogForm()
    context = {
        'form':form
    }
    return HttpResponse(template.render(context, request))

def detail(request, blog_id):
    blog = Blog.objects.get(pk = blog_id)
    context = {
        'blog': blog
    }
    template = loader.get_template('blog/detail.html')
    return HttpResponse(template.render(context, request))
