from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
import csv
from django.http import HttpResponse
from .models import Category
from .forms import CategoryForm
from django.db.models import Count, Q, Sum
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError

def staff_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_staff, login_url='login')(view_func)
    return decorated_view_func

@staff_required
def category_list(request):
    queryset = Category.objects.annotate(
        product_count=Count('product'),
        total_quantity=Sum('product__quantity')
    )
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    # Sorting
    sort = request.GET.get('sort', 'name')
    if sort == 'name':
        queryset = queryset.order_by('name')
    elif sort == '-name':
        queryset = queryset.order_by('-name')
    
    # Pagination
    paginator = Paginator(queryset, 10)  # 10 categories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': CategoryForm(),
        'search_query': search_query,
        'current_sort': sort,
    }
    return render(request, 'categories/category_list.html', context)

# CRUD FUNCTIONS

@staff_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully.')
        else:
            messages.error(request, 'Category creation failed. Please check the fields.')
    return redirect('category_list')

@staff_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if name:
            category.name = name
        if description is not None:  # Allow empty string for description
            category.description = description
        
        try:
            category.full_clean()  # Validate the model
            category.save()
            messages.success(request, 'Category updated successfully.')
        except ValidationError as e:
            messages.error(request, f'Category update failed: {", ".join(e.messages)}')
    return redirect('category_list')

@staff_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
    return redirect('category_list')

# CSV RELATED FUNCTIONS

@staff_required
def import_categories_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.lower().endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
            return redirect('category_list')

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        required_columns = {'name', 'description'}
        if not required_columns.issubset(map(str.lower, reader.fieldnames)):
            messages.error(request, 'CSV file must contain Name and Description columns matching the Category model.')
            return redirect('category_list')

        try:
            for row in reader:
                Category.objects.update_or_create(
                    name=row['name'],
                    defaults={'description': row['description']}
                )
        except Exception as e:
            messages.error(request, f'Error processing CSV file: {str(e)}')
            return redirect('category_list')

        messages.success(request, 'Categories imported successfully.')
    return redirect('category_list')

@staff_required
def export_categories_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="categories_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Description'])

    categories = Category.objects.all()
    if categories.exists():
        for category in categories:
            writer.writerow([category.name, category.description])
        messages.success(request, 'Categories exported successfully.')
    else:
        messages.warning(request, 'No categories found to export.')

    return response