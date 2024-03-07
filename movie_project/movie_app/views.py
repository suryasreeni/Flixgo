from django.http import Http404
from . models import category,products,User
from .forms import ProductForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Comment, Rating
from .forms import CommentForm, RatingForm
from django.contrib.auth import get_user_model
User = get_user_model()
from .forms import CustomUserChangeForm
from django.urls import reverse

from django.core.paginator import Paginator,EmptyPage,InvalidPage




from django.utils.functional import SimpleLazyObject
from django.utils.functional import LazyObject
from django.contrib.auth import get_user_model


def allProdCat(request,c_slug=None,id=None):
    c_page=None
    product=None
    if c_slug!=None:
        c_page=get_object_or_404(category,slug=c_slug)
        product=products.objects.all().filter(category_id=c_page)
    else:
        product=products.objects.all().filter()

    return render(request,"category.html",{'category':c_page,'products':product})


def proDetail(request, c_slug, product_slug):
    try:
        product = products.objects.get(category_id__slug=c_slug, slug=product_slug)
    except products.DoesNotExist:
        raise Http404("Product does not exist")

    return render(request, 'product.html', {'product': product})

from django.contrib.auth import get_user_model
@login_required

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)

            if not isinstance(request.user, get_user_model()):
                # Fetch the user instance based on the provided user information
                user_instance = get_user_model().objects.get(username=request.user.username)
                product.user = user_instance
            else:
                product.user = request.user

            product.save()
            return redirect('/')  # Redirect to the 'allProdCat' page
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})
@login_required
def edit_product(request, id):
    product = get_object_or_404(products, id=id)

    if request.user == product.user:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect(reverse('movie_app:prodCatdetail', args=[product.category_id.slug, product.slug]))
        else:
            form = ProductForm(instance=product)

        return render(request, 'edit_product.html', {'form': form, 'product': product})
    else:
        return redirect('/')
@login_required

def delete_product(request, id):
    product = get_object_or_404(products, id=id)

    # Check if the requesting user is the one who added the product
    if request.user == product.user:
        if request.method == 'POST':
            product.delete()
            return redirect('/')  # Redirect to the 'allProdCat' page
        else:
            return render(request, 'delete_product.html', {'product': product})
    else:
        return redirect('/')  # Redirect to the 'allProdCat' page

@login_required


def add_comment(request, product_id):
    product = products.objects.get(id=product_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Ensure the user is authenticated
            if not request.user.is_authenticated:
                return redirect('login')  # Redirect to login if the user is not authenticated

            # Get the User instance explicitly
            user_instance = get_user_model().objects.get(pk=request.user.pk)

            comment = form.save(commit=False)
            comment.user = user_instance
            comment.product = product
            comment.save()
            return redirect(reverse('movie_app:prodCatdetail', args=[product.category_id.slug, product.slug]))

    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {'form': form, 'product': product})
@login_required
def add_rating(request, product_id):
    product = products.objects.get(id=product_id)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            # Ensure the user is authenticated
            if not request.user.is_authenticated:
                return redirect('login')  # Redirect to login if the user is not authenticated

            # Get the User instance explicitly
            user_instance = get_user_model().objects.get(pk=request.user.pk)

            rating = form.save(commit=False)
            rating.user = user_instance
            rating.product = product
            rating.save()
            return redirect(reverse('movie_app:prodCatdetail', args=[product.category_id.slug, product.slug]))

    else:
        form = RatingForm()

    return render(request, 'add_rating.html', {'form': form, 'product': product})


@login_required

def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/edit_profile')  # Redirect to the user's profile page
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})
