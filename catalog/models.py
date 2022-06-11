from email.policy import default
from pyexpat import model
from statistics import mode
from time import time
import django
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import date
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


# Модель "Книга"
class Book(models.Model):
    """
    Book:
        title
        image
        slug
        author
        description
        price
        format
        writing_date
        language
        tag
    """
    # название
    title = models.CharField(
        max_length=200,  # максимальная длина поля
        help_text='Введите название книги',
        blank=False,  # поле необходимо ввести обязательно
        verbose_name='Название',  # удобночитаемое название
    )

    image = models.ImageField(upload_to='./static/images/book/', blank=True, default='./static/images/default.png')

    slug = models.SlugField(max_length=200, blank=True, unique=True)

    # автор
    author = models.ManyToManyField('Author', verbose_name='Автор', related_name='books')

    # описание
    description = models.TextField(
        max_length=1000,
        help_text='Введите описание книги',
        blank=False,
        verbose_name='Описание',
        default='Описание отсутствует.',
    )

    # цена
    price = models.DecimalField(
        decimal_places=2,  # кол-во цифр после запятой
        max_digits=13,  # максимальное кол-во цифр в числе
        help_text='Введите цену книги',
        blank=False,
        verbose_name='Цена',
        default=0,
    )

    # формат: аудио или текст
    txt = 'TXT'
    audio = 'AUDIO'
    FORMAT_CHOICES = [
        (audio, 'Аудио'),
        (txt, 'Текст'),
    ]

    format = models.CharField(
        max_length=20,
        help_text='Выберите формат книги: аудио или текст',
        blank=False,
        choices=FORMAT_CHOICES,
        default=txt,
        verbose_name='Формат',
    )

    # дата написания
    writing_date = models.DateField(
        help_text='Введите дату написания книги: yyyy-mm-dd',
        verbose_name='Дата написания',
        default=django.utils.timezone.now,
        blank=False,
    )

    # язык
    rus = 'Русский'
    eng = 'Английский'
    LANGUAGE_CHOICES = [
        (rus, rus),
        (eng, eng)
    ]
    language = models.CharField(
        max_length=20,
        help_text='Выберите язык книги',
        blank=False,
        choices=LANGUAGE_CHOICES,
        default=rus,
        verbose_name='Язык',
    )

    # тэги
    tag = models.ManyToManyField('Tag', verbose_name='Тэг', related_name='books')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('book_detail_url', kwargs={'slug': self.slug})

    def get_image_url(self):
        return self.image.url

    def get_update_url(self):
        return reverse('book_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('book_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)


# Модель "Автор"
class Author(models.Model):
    """
    Author:
        name
        slug
        image
        date_of_birth
        date_of_death
        description
    """
    # ФИО автора
    name = models.CharField(
        max_length=200,
        blank=False,
        help_text='Введите ФИО (или псевдоним) автора',
        verbose_name='ФИО',
    )

    slug = models.SlugField(max_length=200, blank=True, unique=True)

    image = models.ImageField(upload_to='./static/images/author/', blank=True, 
        default='./static/images/default.png')

    # дата рождения
    date_of_birth = models.DateField(
        help_text='Введите дату рождения автора: yyyy-mm-dd',
        verbose_name='Дата рождения',
        default=django.utils.timezone.now,
        blank=False,
    )

    # дата смерти
    # date_of_death = models.DateField(
    #     help_text='Введите дату смерти автора: yyyy-mm-dd',
    #     verbose_name='Дата смерти',
    #     default=django.utils.timezone.now,
    #     blank=False,
    # )

    # краткое описание
    description = models.TextField(
        max_length=1000,
        help_text='Введите описание автора',
        blank=False,
        verbose_name='Описание',
        default='Описание отсутствует.',
    )

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('author_detail_url', kwargs={'slug': self.slug})

    def get_image_url(self):
        return self.image.url

    def get_update_url(self):
        return reverse('author_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('author_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)


# Модель "Список тегов у книги"
class Tag(models.Model):
    """
    Tag
        name
        slug
        description
    """
    # тэги
    fantasy = 'Фантастика'  # фантастика
    advanture = 'Приключение'  # приключения
    roman = 'Роман'  # роман
    humor = 'Юмор'  # юмор
    history = 'История'  # история
    love_story = 'Любовный роман'  # любовный роман
    triller = 'Триллер'  # триллер
    psyhology = 'Психология'  # психология
    realism = 'Реализм'  # реализм
    post_ap = 'Пост-апокалипсис'  # пост-апокалипсис
    mistik = 'Мистика'  # мистика
    kids = 'Для детей'  # детские
    learn = 'Обучение'  # обучение

    TAG_CHOICES = [
        (fantasy, fantasy),
        (advanture, advanture),
        (roman, roman),
        (humor, humor),
        (history, history),
        (love_story, love_story),
        (triller, triller),
        (psyhology, psyhology),
        (realism, realism),
        (post_ap, post_ap),
        (mistik, mistik),
        (kids, kids),
        (learn, learn),
    ]

    # название тэга
    name = models.CharField(
        max_length=100,
        blank=False,
        verbose_name='Тэг',
        help_text='Введите название тэга',
        choices=TAG_CHOICES,
    )

    slug = models.SlugField(max_length=100, unique=True, blank=True)

    # краткое описание
    description = models.TextField(
        max_length=1000,
        help_text='Введите описание тэга',
        blank=False,
        verbose_name='Описание',
        default='Описание отсутствует.',
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)


# Модель "Цитата"
class Quote(models.Model):
    """
    Quote
        text
        slug
        author
        book
    """
    # текст цитаты
    text = models.TextField(
        max_length=1000,
        help_text='Введите текст цитаты',
        blank=False,
        verbose_name='Текст цитаты',
    )

    slug = models.SlugField(max_length=200, blank=True, unique=True)

    #image = models.ImageField(upload_to='./static/images/quote/', default='./static/images/default.png')

    # автор
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    # книга, откуда берется цитата
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Цитата'
        verbose_name_plural = 'Цитаты'
        ordering = ['author']

    def get_absolute_url(self):
        return reverse('quote_detail_url', kwargs={'slug': self.slug})

    # def get_image_url(self):
    #     return self.image.url

    def get_update_url(self):
        return reverse('quote_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('quote_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.author)
        super().save(*args, **kwargs)


# Модель "Любимый автор пользователя"
class FavoriteQuote(models.Model):
    # пользователь
    user = models.CharField(max_length=255, default=None, blank=False, null=True)

    # цитата
    # quote = models.ForeignKey('Quote', on_delete=models.DO_NOTHING)
    quote = models.CharField(max_length=255, default=None, blank=False, null=True)

    # session_key = models.CharField(max_length=128, default=None, blank=False, null=True)

    class Meta:
        verbose_name = 'Любимая цитата пользователя'
        verbose_name_plural = 'Любимые цитаты пользователей'
        ordering = ['user']

    def get_absolute_url(self):
        return Quote.objects.get(text=self.quote).get_absolute_url()

    def get_book(self):
        return Quote.objects.get(text=self.quote).book

    def get_author(self):
        return Quote.objects.get(text=self.quote).author

    def get_text(self):
        return Quote.objects.get(text=self.quote).text

    def __str__(self):
        return str(self.user) + ' ' + str(self.quote)


# Модель "Любимый автор пользователя"
class FavoriteAuthor(models.Model):
    # пользователь
    # user = 'add_user_here'
    user = models.CharField(max_length=255, default=None, blank=False, null=True)

    # автор
    # author = models.ForeignKey('Author', on_delete=models.DO_NOTHING)
    author = models.CharField(max_length=255, default=None, blank=False, null=True)

    # session_key = models.CharField(max_length=128, default=None, blank=False, null=True)

    class Meta:
        verbose_name = 'Любимый автор пользователя'
        verbose_name_plural = 'Любимые авторы пользователей'
        ordering = ['author']

    def get_absolute_url(self):
        return Author.objects.get(name=self.author).get_absolute_url()

    def get_name(self):
        return Author.objects.get(name=self.author).name

    def get_date_of_birth(self):
        return Author.objects.get(name=self.author).date_of_birth
    
    def get_image(self):
        return Author.objects.get(name=self.author).get_image_url()

    def __str__(self):
        return str(self.user) + ' ' + str(self.author)


# Модель "Список купленных книг пользователя"
class PurchasedBook(models.Model):
    # пользователь
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.CharField(max_length=255, default=None, blank=False, null=True)

    # книга
    # book = models.ForeignKey('Book', on_delete=models.DO_NOTHING)
    book = models.CharField(max_length=255, default=None, blank=False, null=True)

    # session_key = models.CharField(max_length=128, default=None, blank=False, null=True)

    class Meta:
        verbose_name = 'Купленная книга пользователя'
        verbose_name_plural = 'Купленные книги пользователей'
        ordering = ['book']

    def get_absolute_url(self):
        return Book.objects.get(title=self.book).get_absolute_url()

    def get_title(self):
        return Book.objects.get(title=self.book).title

    def get_price(self):
        return Book.objects.get(title=self.book).price
    
    def get_image(self):
        return Book.objects.get(title=self.book).get_image_url()

    def get_user(self):
        return self.user

    def __str__(self):
        return str(self.user) + ' ' + str(self.book)


# Модель "Любимые книги пользователя"
class FavoriteBook(models.Model):
    # пользователь
    #user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.CharField(max_length=255, default=None, blank=False, null=True)

    # книга
    #book = models.ForeignKey('Book', on_delete=models.DO_NOTHING)
    book = models.CharField(max_length=255, default=None, blank=False, null=True)

    # session_key = models.CharField(max_length=128, default=None, blank=False, null=True)

    class Meta:
        verbose_name = 'Любимая книга пользователя'
        verbose_name_plural = 'Любимые книги пользователей'
        ordering = ['book']

    def get_absolute_url(self):
        return Book.objects.get(title=self.book).get_absolute_url()

    def get_title(self):
        return Book.objects.get(title=self.book).title

    def get_price(self):
        return Book.objects.get(title=self.book).price
    
    def get_image(self):
        return Book.objects.get(title=self.book).get_image_url()

    def __str__(self):
        return str(self.user) + ' ' + str(self.book)



# Модель "Авторы книги"
# class AuthorBook(models.Model):
#     # книга
#     book = models.ForeignKey('Book', on_delete=models.CASCADE)

#     # автор
#     author = models.ForeignKey('Author', on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = 'Авторы книги'
#         verbose_name_plural = 'Авторы книг'
#         ordering = ['author']

#     def get_absolute_url(self):
#         return reverse('authorbook_detail', args=[str(self.id)])

#     def __str__(self):
#         return self.book + self.author


# Модель "Заказ"
# class Buy(models.Model):
#     """
#     Buy
#         user
#         slug
#         cost
#         date
#         composition
#     """
#     # пользователь
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)

#     slug = models.SlugField(max_length=200, blank=True, unique=True)

#     # стоимость
#     cost = models.DecimalField(
#         decimal_places=2,  # кол-во цифр после запятой
#         max_digits=13,  # максимальное кол-во цифр в числе
#         help_text='Введите стоимость заказа',
#         #blank=False,
#         verbose_name='Стоимость',
#         default=0,
#     )

#     # дата
#     date = models.DateField(
#         help_text='Введите дату создания заказа: yyyy-mm-dd',
#         verbose_name='Дата заказа',
#         default=django.utils.timezone.now,
#         blank=False,
#     )

#     # состав заказа
#     composition = models.ManyToManyField(Book, verbose_name='Состав заказа')

#     class Meta:
#         verbose_name = 'Заказ'
#         verbose_name_plural = 'Заказы'
#         ordering = ['cost']

#     def get_absolute_url(self):
#         return reverse('buy_detail_url', kwargs={'slug': self.slug})

#     def get_update_url(self):
#         return reverse('buy_update_url', kwargs={'slug': self.slug})

#     def get_delete_url(self):
#         return reverse('buy_delete_url', kwargs={'slug': self.slug})

#     def __str__(self):
#         return "Заказ " + str(self.user) + " от " + self.get_date() + " на сумму " + str(self.get_buy_cost()) + " руб."

#     # рассчитать сумму заказа
#     def get_buy_cost(self):
#         cost = 0
#         for book in self.composition.all():
#             cost += book.price
#         #cost *= self.client.sale.discount
#         cost = round(cost, 2)
#         self.cost = cost
#         self.save()
#         return cost

#     def get_date(self):
#         return str(self.date)

#     def save(self, *args, **kwargs):
#         if not self.id:
#             self.slug = gen_slug(self.user)
#         super().save(*args, **kwargs)


# Модель "Состав заказа"
# class BuyComposition(models.Model):
#     # заказ
#     buy = models.ForeignKey('Buy', on_delete=models.DO_NOTHING)

#     # книга
#     book = models.ForeignKey('Book', on_delete=models.DO_NOTHING)

#     class Meta:
#         verbose_name = 'Состав заказ'
#         verbose_name_plural = 'Составы заказов'
#         ordering = ['buy']

#     def __str__(self):
#         return self.buy

#     def get_absolute_url(self):
#         return reverse('buycomposition_detail', args=[str(self.id)])


# Модель "Издатель"
# class Publisher(models.Model):
#     """
#     Publisher
#         name
#         image
#         slug
#         description
#         book
#     """
#     # название издателя
#     name = models.CharField(
#         max_length=200,
#         blank=False,
#         verbose_name='Издатель',
#         help_text='Введите название издателя'
#     )

#     image = models.ImageField(upload_to='./static/images/publisher/', default='./static/images/default.png')

#     slug = models.SlugField(max_length=200, blank=True, unique=True)

#     # описание
#     description = models.TextField(
#         max_length=1000,
#         help_text='Введите описание издателя',
#         blank=False,
#         verbose_name='Описание',
#         default='Описание отсутствует.',
#     )

#     # книги издателя
#     books = models.ManyToManyField('Book', verbose_name='Книги', related_name='publishers')

#     class Meta:
#         verbose_name = 'Издатель'
#         verbose_name_plural = 'Издатели'
#         ordering = ['name']

#     def get_absolute_url(self):
#         return reverse('publisher_detail_url', kwargs={'slug': self.slug})

#     def get_update_url(self):
#         return reverse('publisher_update_url', kwargs={'slug': self.slug})

#     def get_delete_url(self):
#         return reverse('publisher_delete_url', kwargs={'slug': self.slug})

#     def get_image_url(self):
#         return self.image.url

#     def __str__(self):
#         return self.name

#     def save(self, *args, **kwargs):
#         if not self.id:
#             self.slug = gen_slug(self.name)
#         super().save(*args, **kwargs)


# Модель "Список книг у издателя"
# class PublisherBook(models.Model):
#     # издатель
#     publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)

#     # книга
#     book = models.ForeignKey('Book', on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = 'Список книг у издателя'
#         verbose_name_plural = 'Списки книг у издателей'
#         ordering = ['publisher']

#     def get_absolute_url(self):
#         return reverse('publisherbook_detail', args=[str(self.id)])

#     def __str__(self):
#         return self.publisher + self.book


# Модель "Скидка"
# class Coupon(models.Model):
#     """
#     Coupon
#         name
#         slug
#         description
#         discount
#     """
#     # Название купона
#     name = models.CharField(
#         max_length=200,
#         help_text='Введите название купона',
#         verbose_name='Купон',
#         blank=False,
#     )

#     slug = models.SlugField(max_length=200, blank=True, unique=True)

#     #image = models.ImageField(upload_to='./static/images/coupon/', default='./static/images/default.png')

#     # описание (условия применения купона здесь же)
#     description = models.TextField(
#         max_length=1000,
#         help_text='Введите описание купона',
#         blank=False,
#         verbose_name='Описание',
#     )

#     # Cкидка по купону
#     discount = models.PositiveSmallIntegerField(
#         default=0,
#         help_text='Введите скидку по купону в %',
#         verbose_name='Скидка по купону',
#         validators=[
#             MinValueValidator(0),
#             MaxValueValidator(100)
#         ]
#     )

#     class Meta:
#         verbose_name = 'Купон'
#         verbose_name_plural = 'Купоны'
#         ordering = ['name']

#     def get_absolute_url(self):
#         return reverse('coupon_detail_url', kwargs={'slug': self.slug})

#     # def get_image_url(self):
#     #     return self.image.url

#     def get_update_url(self):
#         return reverse('coupon_update_url', kwargs={'slug': self.slug})

#     def get_delete_url(self):
#         return reverse('coupon_delete_url', kwargs={'slug': self.slug})

#     def __str__(self):
#         return 'Купон "' + str(self.name) + '" со скидкой ' + str(self.discount) + '%'

#     def get_discount_coef(self):
#         disc = 1 - self.discount / 100
#         return disc

#     def save(self, *args, **kwargs):
#         if not self.id:
#             self.slug = gen_slug(self.name)
#         super().save(*args, **kwargs)
