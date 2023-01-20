from django.db import models
from django.urls import reverse


class Brand(models.Model):
    brand_name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", null=True)

    def __str__(self):
        return self.brand_name

    class Meta:  # Используется в админ-панели
        verbose_name = 'Брэнды'
        verbose_name_plural = 'Брэнды'
        ordering = ['id']


class Category(models.Model):
    category_name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", null=True)

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    class Meta:  # Используется в админ-панели
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.subcategory_name

    def get_absolute_url(self):
        return reverse('subcategory', kwargs={'subcategory_slug': self.slug})

    class Meta:  # Используется в админ-панели
        verbose_name = 'Подкатегории'
        verbose_name_plural = 'Подкатегории'
        ordering = ['id']


class Clothes(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", null=True)
    content = models.TextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    photo = models.ImageField(upload_to='pictures/%y/%m/%d/', verbose_name='Фото')
    alternative_photo = models.ImageField(upload_to='alternative-pictures/%y/%m/%d/', null=True, verbose_name='Фото 2')
    time_create = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=255, null=True, verbose_name='Пол')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='Брэнд')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, null=True, verbose_name='Подкатегория')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, verbose_name='Категория')

    def __str__(self):
        return self.title

    class Meta:  # Используется в админ-панели
        verbose_name = 'Вещи'
        verbose_name_plural = 'Вещи'
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})
