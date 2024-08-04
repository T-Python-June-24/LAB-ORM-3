from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from products.models import Product  # Make sure to import the Product model
from .forms import CategoryForm
from django.contrib import messages

def all_categories(request):

    categories = Category.objects.all()
    if not categories :

        messages.error(request, "No categories to display. Add the first one now!", "info")

    return render(request, 'categories/all_categories.html', {'categories': categories})

def add_category(request):

    try:
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()

                messages.success(request, "Added category successfully", "success")
            else:
                messages.error(request, "Couldn't Add category", "danger")
        else:
            form = CategoryForm()
    except Exception as e :
        print("Error: ",e)
        messages.error(request, "Couldn't Add category", "danger")

    return redirect('categories:all_categories')

def category_update(request, category_id):


    try:
        category = Category.objects.get(pk=category_id)

        if request.method == 'POST':
            form = CategoryForm(request.POST, request.FILES, instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, "Updated category successfully", "success")
            else:
                messages.error(request, "Couldn't Update category", "danger")

    except Exception as e :
        print("Error: ",e)
        messages.error(request, "Couldn't Update category", "danger")

    return redirect('categories:all_categories')


def category_delete(request, category_id):

    try:
        category = get_object_or_404(Category, pk=category_id)

        if request.method == 'POST':
            category.delete()
            messages.success(request, "Deleted category successfully", "success")
    except Exception as e :
        print("Error: ",e)
        messages.error(request, "Couldn't Delete category", "danger")

    return redirect('categories:all_categories')

