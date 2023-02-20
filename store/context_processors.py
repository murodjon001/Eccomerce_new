from .models import Category, Product

def categories(request):
    return {
        'categories': Category.objects.filter(level=0)
    }

