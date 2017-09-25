from django.shortcuts import render
from landing.forms import SubscriberForm
from products.models import Product, ProductImage


def landing(request):
    form = SubscriberForm(request.POST or None)
    if request.POST and form.is_valid():
        form.save()
    return render(request, 'landing.html', locals() )

def home(request):
    products_images = ProductImage.objects.filter(is_active=True, is_main=True)
    return render(request, 'home.html', locals() )