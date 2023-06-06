"""articlesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',main,name='main'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('publication/', publication_view, name='publication'),
    path('success/<int:article_id>/', success_view, name='success'),
    path('articles/<int:id>/', article_detail_view, name='article_detail'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main'), name='logout'),
    path('category/<int:category_id>/', category_detail, name='category'),
    path('favorites/', favorites_view, name='favorites'),
    path('reviews/<int:article_id>/', reviews_view, name='reviews'),
    path('add_review/<int:article_id>/', add_review_view, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
