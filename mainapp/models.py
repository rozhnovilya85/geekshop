from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name='Название')
    image = models.ImageField(upload_to='products/', blank=True)
    short_desc = models.CharField(max_length=255, blank=True)
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits =8, decimal_places=2, verbose_name='Цена', default=0)
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'




