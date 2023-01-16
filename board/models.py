from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, blank=True, verbose_name="Фамилия")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="Имя")
    email = models.EmailField(blank=True, verbose_name="email")
    is_active = models.BooleanField(default=True,)

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('author', kwargs={'author_id': self.pk})

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['id']


class Articles(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    title = models.CharField(max_length=255, verbose_name="Название")
    text = models.TextField(blank=True, verbose_name="Текст статьи")
    cat = models.ForeignKey('Category',
        max_length=15,
        on_delete=models.PROTECT,
        default='tank',
        verbose_name="Категория"
    )
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    video = models.FileField(upload_to='uploads/', verbose_name="Видео")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    rating = models.SmallIntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['date_create', 'title']

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('tank', 'Танки'),
        ('heal', 'Хилы'),
        ('dd', 'ДД'),
        ('sales', 'Торговцы'),
        ('gildenmaster', 'Гилдмастеры'),
        ('guest', 'Квестгиверы, '),
        ('blacksmiths', 'Кузнецы'),
        ('skinner', 'Кожевники'),
        ('potions', 'Зельевары'),
        ('spell masters', 'Мастера заклинаний'),
    ]
    name = models.CharField(max_length=100, db_index=True, choices=CATEGORY_CHOICES, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class CommentArticles(models.Model):
    commentArticles = models.ForeignKey(Articles, on_delete=models.CASCADE, default="Free", related_name='comments_articles')
    commentAuthor = models.ForeignKey(Author, on_delete=models.CASCADE, default="Free", verbose_name='Автор комментария')
    text = models.TextField(verbose_name="Текст комментария", max_length=500)
    dateCreation = models.DateTimeField("Добавлен", auto_now_add=True)

    def __str__(self):
        return self.text


