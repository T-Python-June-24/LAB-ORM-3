import csv
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from .forms import CategoryForm
from django.core.paginator import Paginator
from django.contrib import messages

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories:list_categories')
    else:
        form = CategoryForm()
    
    return render(request, 'categories/add_category.html', {'form': form})

def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories:list_categories')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'categories/edit_category.html', {'form': form})

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('categories:list_categories')
    
    return render(request, 'categories/delete_category.html', {'category': category})

def list_categories(request):
    categories_list = Category.objects.order_by('id').all()
    paginator = Paginator(categories_list, 10)  # Show 10 categories per page
    page_number = request.GET.get('page')
    categories = paginator.get_page(page_number)
    return render(request, 'categories/list_categories.html', {'categories': categories})




def import_categories_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            messages.error(request, 'Please upload a CSV file.')
            return render(request, 'categories/import_categories.html')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file.')
            return render(request, 'categories/import_categories.html')

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                try:
                    Category.objects.create(
                        name=row['name'],
                        description=row.get('description', '')
                    )
                except Exception as e:
                    messages.error(request, f'Error saving category {row["name"]}: {e}')
                    continue

            messages.success(request, 'Categories imported successfully.')
            return redirect('categories:list_categories')

        except Exception as e:
            messages.error(request, f'Error processing CSV file: {e}')

    return render(request, 'Categories/import_categories_csv.html')
