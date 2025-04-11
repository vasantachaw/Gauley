from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from bs4 import BeautifulSoup


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = CKEditor5Field(config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_images_from_content(self):
        soup = BeautifulSoup(self.content, 'html.parser')
        images = soup.find_all('img')  # Find all <img>
        image_urls = [img['src'] for img in images if 'src' in img.attrs]
        return image_urls
