import datetime

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


class Sizes(models.Model):
    size_title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    size = models.CharField(max_length=255)

    def __str__(self):
        return self.size_title

    # def get_absolute_url(self):
    #     return reverse('size', kwargs={'size_slug': self.slug})

    class Meta:  # Используется в админ-панели
        verbose_name = 'Размеры'
        verbose_name_plural = 'Размеры'
        ordering = ['id']


class Clothes(models.Model):
    Man = 'Man'
    Woman = 'Woman'
    All = 'All'
    GENDERS = [
        (Man, 'Для мужчин'),
        (Woman, 'Для женщин'),
        (All, 'Унисекс'),
    ]

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", null=True)
    content = models.TextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    photo = models.ImageField(upload_to='pictures/%y/%m/%d/', verbose_name='Фото')
    alternative_photo = models.ImageField(upload_to='alternative-pictures/%y/%m/%d/', blank=True, null=True,
                                          verbose_name='Фото 2')
    time_create = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=5, choices=GENDERS, default=All, verbose_name='Пол')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='Брэнд')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, null=True, verbose_name='Подкатегория')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, verbose_name='Категория')
    sizes = models.ManyToManyField(Sizes, through='Sizes_of_Clothes')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вещи'
        verbose_name_plural = 'Вещи'
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})


class Sizes_of_Clothes(models.Model):
    id_clothes = models.ForeignKey(Clothes, on_delete=models.PROTECT, verbose_name='id товара')
    id_size = models.ForeignKey(Sizes, on_delete=models.PROTECT, verbose_name='id размера')
    count = models.IntegerField(verbose_name='Кол-во')

    def __str__(self):
        return self.id_clothes.title + ' (' + self.id_size.size_title + ')'

    class Meta:
        verbose_name = 'Размеры вещей'
        verbose_name_plural = 'Размеры вещей'
        ordering = ['id']


class Orders(models.Model):
    OK = 'Ok'
    CANCELED = 'Canceled'
    PROGRESS = 'In progress'
    STATUS = [
        (OK, 'Исполнено'),
        (CANCELED, 'Отменен'),
        (PROGRESS, 'В процессе'),
    ]

    user_name = models.CharField(max_length=255, default=None, verbose_name='Пользователь')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Принят в исполнение')
    status = models.CharField(max_length=11, choices=STATUS, default=PROGRESS, verbose_name='Статус')
    time_accept = models.DateTimeField(auto_now_add=False, default=datetime.datetime.now() + datetime.timedelta(days=1),
                                       verbose_name='Принят в пункте выдачи')
    product = models.ManyToManyField(Sizes_of_Clothes, through='Orders_of_Clothes', verbose_name='Товар')
    total_price = models.IntegerField(verbose_name='Общая стоимость', default=0)

    class Meta:
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказы'
        ordering = ['id']


class Orders_of_Clothes(models.Model):
    id_clothes_with_size = models.ForeignKey(Sizes_of_Clothes, on_delete=models.PROTECT, verbose_name='id товара')
    id_order = models.ForeignKey(Orders, on_delete=models.PROTECT, verbose_name='id размера')
    count = models.IntegerField(verbose_name='Кол-во', default=1)

    class Meta:
        verbose_name = 'Наполнение заказов'
        verbose_name_plural = 'Наполнение заказов'
        ordering = ['id']
