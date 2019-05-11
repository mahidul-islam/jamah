from django.shortcuts import render
from .models import Sales, Product
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader


def detailProduct(request, pk):
    pass

def allProduct(request):
    return HttpResponse('This is allProduct page')

def productInRange(request, lowrange, highrange):
    products = Product.objects.all()
    print(products)
    rangedProduct = [n for n in products if n.price<highrange if n.price>lowrange]
    print(rangedProduct)
    context = {'rangedProduct': rangedProduct,'lowrange': lowrange, 'highrange':  highrange}
    template = loader.get_template('product/productInRange.html')
    return HttpResponse(template.render(context, request))
