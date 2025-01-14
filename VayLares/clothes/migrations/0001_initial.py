# Generated by Django 4.1.2 on 2023-03-10 14:51

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=255, null=True, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Брэнды',
                'verbose_name_plural': 'Брэнды',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=255, null=True, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категории',
                'verbose_name_plural': 'Категории',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Clothes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=255, null=True, unique=True, verbose_name='URL')),
                ('content', models.TextField(verbose_name='Описание')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('photo', models.ImageField(upload_to='pictures/%y/%m/%d/', verbose_name='Фото')),
                ('alternative_photo', models.ImageField(blank=True, null=True, upload_to='alternative-pictures/%y/%m/%d/', verbose_name='Фото 2')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('gender', models.CharField(choices=[('Man', 'Для мужчин'), ('Woman', 'Для женщин'), ('All', 'Унисекс')], default='All', max_length=5, verbose_name='Пол')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clothes.brand', verbose_name='Брэнд')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='clothes.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Вещи',
                'verbose_name_plural': 'Вещи',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(default=None, max_length=255, verbose_name='Пользователь')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Принят в исполнение')),
                ('status', models.CharField(choices=[('Ok', 'Исполнено'), ('Canceled', 'Отменен'), ('In progress', 'В процессе')], default='In progress', max_length=11, verbose_name='Статус')),
                ('time_accept', models.DateTimeField(default=datetime.datetime(2023, 3, 11, 17, 51, 18, 724958), verbose_name='Принят в пункте выдачи')),
                ('total_price', models.IntegerField(default=0, verbose_name='Общая стоимость')),
            ],
            options={
                'verbose_name': 'Заказы',
                'verbose_name_plural': 'Заказы',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Sizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_title', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('size', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Размеры',
                'verbose_name_plural': 'Размеры',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory_name', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=255, null=True, unique=True, verbose_name='URL')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clothes.category')),
            ],
            options={
                'verbose_name': 'Подкатегории',
                'verbose_name_plural': 'Подкатегории',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Sizes_of_Clothes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='Кол-во')),
                ('id_clothes', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clothes.clothes', verbose_name='id товара')),
                ('id_size', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clothes.sizes', verbose_name='id размера')),
            ],
            options={
                'verbose_name': 'Размеры вещей',
                'verbose_name_plural': 'Размеры вещей',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Orders_of_Clothes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1, verbose_name='Кол-во')),
                ('id_clothes_with_size', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clothes.sizes_of_clothes', verbose_name='id товара')),
                ('id_order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clothes.orders', verbose_name='id размера')),
            ],
            options={
                'verbose_name': 'Наполнение заказов',
                'verbose_name_plural': 'Наполнение заказов',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='orders',
            name='product',
            field=models.ManyToManyField(through='clothes.Orders_of_Clothes', to='clothes.sizes_of_clothes', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='clothes',
            name='sizes',
            field=models.ManyToManyField(through='clothes.Sizes_of_Clothes', to='clothes.sizes'),
        ),
        migrations.AddField(
            model_name='clothes',
            name='subcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='clothes.subcategory', verbose_name='Подкатегория'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('gender', models.CharField(choices=[('Мужcкой', 'Мужcкой'), ('Женский', 'Женский')], default='Мужcкой', max_length=15)),
                ('image', models.ImageField(blank=True, null=True, upload_to='user-images')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователи',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
