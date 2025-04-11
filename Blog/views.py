from django.shortcuts import render
from Blog.models import Article
def blog_post(request):
    return render(request, 'Blog/blogs.html')
def blog_view(request,pk):
    blog_content=Article.objects.get(pk=pk)
    context={'blog_content':blog_content}
    return render(request,'Blog/blog_view.html',context)