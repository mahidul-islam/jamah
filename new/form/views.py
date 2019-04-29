from django.shortcuts import render
from .models import Sales, Product

def detailProduct(request, pk):
    pass

def allProduct(request):
    pass

def productInRange(request, lowrange, highrange):
    products = Product.objects.all()
    print(products)
    rangedProduct = [n for n in products if n.price<highrange if n.price>lowrange]
    print(rangedProduct)
    context = {'rangedProduct': rangedProduct,'lowrange': lowrange, 'highrange':  highrange}
    return render(request, 'product/productInRange.html', context)
