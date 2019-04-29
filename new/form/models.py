from django.db import models

class Product(models.Model):
    name = models.CharField(max_length = 50)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)

    def __str__(self):
        return self.name

class Sales(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    timestamp = models.DateField()

    def __str__(self):
        return '(Sales of {})'.format(self.product.name)
