from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Blog.views import blog_post,blog_view
urlpatterns=[
path('blog/',blog_post,name='blog_post'),
path('blog/<int:pk>',blog_view,name='blog_view')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
