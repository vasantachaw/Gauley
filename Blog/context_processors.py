from Blog.models import Article
from django.shortcuts import render
def blog(request):
    # Example of getting all articles
    articles = Article.objects.all()

    # Extract images from content for each article
    for article in articles:
        article.image_urls = article.get_images_from_content()

    # Pass articles with image URLs to the context
    return {'articles': articles[:3]}