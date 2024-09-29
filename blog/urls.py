from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogListView, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView
from django.views.decorators.cache import cache_page

app_name = BlogConfig.name

urlpatterns = [
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('', cache_page(60)(BlogListView.as_view()), name='blog_list'),
    path('view/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
]