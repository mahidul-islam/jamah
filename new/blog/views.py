from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Blog
from django.contrib import messages


def allblog(request):
    blogs = Blog.objects.all()
    context = {
        'blogs':blogs
    }
    template = loader.get_template('blog/allblog.html')
    return HttpResponse(template.render(context, request))

def create(request):
    if request.POST:
        heading = request.POST['heading']
        body = request.POST['body']
        is_finished = False
        published = False
        if len(request.POST.getlist('is_finished')):
            finished = request.POST.getlist('is_finished')
            is_finished = finished[0]
        if len(request.POST.getlist('published')):
            pub = request.POST.getlist('published')
            published = pub[0]
        blog = Blog(
            heading_text=heading,
            body_text=body,
            is_finished=is_finished,
            is_published=published,
            author = request.user
            ).save()
        messages.success(request, "is double message working")
        messages.add_message(request, messages.SUCCESS, 'Added new BLOG.')
        return HttpResponseRedirect(reverse('blog:allblog'))
    template = loader.get_template('blog/create.html')
    context = {}
    return HttpResponse(template.render(context, request))

def detail(request, blog_id):
    blog = Blog.objects.get(pk = blog_id)
    context = {
        'blog': blog
    }
    template = loader.get_template('blog/detail.html')
    return HttpResponse(template.render(context, request))