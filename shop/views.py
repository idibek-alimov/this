from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Category,Product
from django.views.generic import ListView,CreateView
from django.db.models import Q
# Create your views here.
from cart.forms import CartAddProductForm
def product_list(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category,slug = category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category':category,
                   'categories':categories,
                   'products':products})

def product_detail(request,id,slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product':product,
                   'cart_product_form': cart_product_form})



def search_list(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/search_results.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

class SearchResultsListView(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'shop/product/search.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(
            Q(name__icontains=query) | Q(name__icontains=query)
        )
    #queryset = Product.objects.filter(name__icontains='nike')


class ProductCreateView(CreateView):
    model = Product
    template_name = 'shop/product/product_new.html'
    fields = ('category','name','slug','description','price')
    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
