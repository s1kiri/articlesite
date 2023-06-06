from django.shortcuts import render, redirect
from .models import articles, article_status, category
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from .models import User
from .forms import *
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            error_message = "Неправильный email или пароль. Пожалуйста, попробуйте снова."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.last_name = surname
        user.save()
        
        return redirect('main')
    else:
        return render(request, 'registration.html')

def main(request):
    categories = category.objects.all()
    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name

        full_name = f"{first_name} {last_name}"
    else:
        full_name = ''
    return render(request, 'main.html', {'full_name': full_name, 'categories':categories})

def category_detail(request, category_id):
    category_obj = get_object_or_404(category, id=category_id)
    articles_list = articles.objects.filter(cat=category_obj)
    return render(request, 'category_detail.html', {'category': category_obj, 'articles': articles_list})


from django.contrib.auth.decorators import login_required

from .models import statuses

@login_required
def publication_view(request):
    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name

        full_name = f"{first_name} {last_name}"
    else:
        full_name = ''
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        category_id = request.POST.get('category')
        author_id = request.user.id
        
        article = articles.objects.create(
            cat_id=category_id,
            text=text,
            title=title,
            author_id=author_id
        )
        
        author_status = statuses.objects.get(status='author')
        
        status = article_status.objects.create(
            user_id=request.user,
            article_id=article,
            status_id=author_status
        )
        last_activity = article_status.objects.filter(user_id=request.user, status_id=1).order_by('-id').first()
        return redirect('success', article_id=article.id)
    else:

        categories = category.objects.all()

        return render(request, 'publication.html', {'categories': categories, 'full_name': full_name})


def success_view(request, article_id):

    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name


        full_name = f"{first_name} {last_name}"
    else:
        full_name = ''
    article_url = reverse('article_detail', args=[article_id])
    return render(request, 'success.html', {'article_url': article_url, 'full_name': full_name})

from app.models import User

def article_detail_view(request, id):
    article = get_object_or_404(articles, id=id)
    author = User.objects.get(id=article.author_id)
    author_name = f"{author.first_name} {author.last_name}"

    if request.user.is_authenticated:
        full_name = f"{request.user.first_name} {request.user.last_name}"
        user_id = request.user.id
        article_id = article.id
        status_id = statuses.objects.get(status='favourite').id
        read_id = statuses.objects.get(status='read').id
        is_favorite = article_status.objects.filter(user_id=user_id, article_id=article_id, status_id=status_id).exists()
        read_s = article_status.objects.filter(user_id=user_id, article_id=article_id, status_id=read_id).exists()
        if request.method == 'POST':
            if 'add_favorite' in request.POST:
                if is_favorite:
                    article_status.objects.filter(user_id=user_id, article_id=article_id, status_id=status_id).delete()
                else:
                    article_status.objects.create(user_id_id=user_id, article_id_id=article_id, status_id_id=status_id)
            elif 'mark_read' in request.POST:
                article_status.objects.create(user_id_id=user_id, article_id_id=article_id, status_id_id=read_id)
            elif 'mark_unread' in request.POST:
                article_status.objects.filter(user_id=user_id, article_id=article_id, status_id=read_id).delete()

            return redirect('article_detail', id=id)

    else:
        full_name = ''
        is_favorite = False
        read_s = False
    return render(request, 'article_examples.html', {'article': article, 'author_name': author_name, 'full_name': full_name, 'is_favorite': is_favorite, 'read_s':read_s})

from django.shortcuts import render
from .models import articles, article_status, statuses

def favorites_view(request):
    if request.user.is_authenticated:
        full_name = f"{request.user.first_name} {request.user.last_name}"
        status_id = statuses.objects.get(status='favourite').id
        fav_articles_id = article_status.objects.filter(user_id=request.user.id, status_id=status_id).values_list('article_id', flat=True)
        favorite_articles = articles.objects.filter(id__in=fav_articles_id)
    else:
        full_name = ''
        favorite_articles = []

    return render(request, 'favorites.html', {'favorite_articles': favorite_articles, 'full_name': full_name})

from .models import articles, reviews

def reviews_view(request, article_id):
    article = get_object_or_404(articles, id=article_id)
    reviews_list = reviews.objects.filter(article_id=article_id)
    show_form = article_status.objects.filter(article_id=article_id, user_id=request.user.id, status_id=statuses.objects.get(status='read').id).exists()

    return render(request, 'reviews.html', {'article_id': article_id, 'reviews': reviews_list, 'show_form': show_form, 'article': article})

def add_review_view(request, article_id):
    if request.method == 'POST':
        review_text = request.POST.get('text', '')
        review = reviews.objects.create(article_id_id=article_id, reviewer_id=request.user.id, text=review_text)
        return redirect('reviews', article_id=article_id)


