from django.shortcuts import render
from django.urls import path
from RatingAndReview.views import overReview
from RatingAndReview.views import productReview
urlpatterns = [
    path('review/', overReview, name='review'),
    path('productreview/<int:pk>/', productReview, name='productreview'),
    
]
