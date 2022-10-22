from django.db import models


class Brand(models.Model):
    brand_name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.brand_name


class Category(models.Model):
    category_name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.category_name


class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=100, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.subcategory_name


class Clothes(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    price = models.IntegerField()
    photo = models.ImageField(upload_to='pictures/%y/%m/%d/')
    time_create = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, null=True)
