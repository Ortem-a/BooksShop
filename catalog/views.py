from asyncio.windows_events import NULL
from pyexpat import model
from re import template
from unittest import mock
from urllib import request, response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from matplotlib.pyplot import title
from matplotlib.style import context
from requests import session
from .models import *
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import *
from .utils import *
from django.db.models import Q
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm


def home(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_authors = Author.objects.count()  # Метод 'all()' применён по умолчанию.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Отрисовка HTML-шаблона home.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'home.html',
        context={'num_books': num_books, 'num_authors': num_authors, 'num_visits': num_visits},
    )


class MyRegisterFormView(FormView):
    # Укажем какую форму мы будем использовать для регистрации наших пользователей, в нашем случае
    # это UserCreationForm - стандартный класс Django унаследованный
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = '/'

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "../templates/registration/register.html"

    def form_valid(self, form):
        form.save()
        # Функция super( тип [ , объект или тип ] )
        # Возвратите объект прокси, который делегирует вызовы метода родительскому или родственному классу типа .
        return super(MyRegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(MyRegisterFormView, self).form_invalid(form)



# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# Book
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
def books_list(request):
    search_query = request.GET.get('search', '')

    if (search_query):
        books = Book.objects.filter(Q(title__icontains=search_query))
    else:
        books = Book.objects.all()

    return render(request, 'catalog/book/books_list.html', context={'books': books}) 


class BookDetailView(ObjectDetailMixin, View):
    model = Book
    template = 'catalog/book/book_detail.html'


class BookCreateView(ObjectCreateMixin, View):
    form_model = BookForm
    template = 'catalog/book/book_create_form.html'


class BookUpdateView(ObjectUpdateMixin, View):
    model = Book
    form_model = BookForm
    template = 'catalog/book/book_update_form.html'


class BookDeleteView(ObjectDeleteMixin, View):
    model = Book
    template = 'catalog/book/book_delete_form.html'
    redirect_url = 'books_list_url'


class FavoriteBooksByUserListView(LoginRequiredMixin, ListView):
    model = FavoriteBook
    template_name = 'catalog/book/books_favorite_list.html'

    def get_queryset(self):
        return FavoriteBook.objects.filter(user=self.request.user)

def add_book_to_favorites(request):
    return_dict = dict()
    session_key = request.session.session_key
    # print("\n\n",request.POST,"\n\n")

    already_exist = FavoriteBook.objects.filter(
        user=request.POST.get('user'), 
        book=request.POST.get('book'), 
        # session_key=session_key
    )

    if (not already_exist):
        # print('request.POST:\n', request.POST, '\n\n')

        book_obj = Book.objects.get(title=str(request.POST.get('book')))
        user_obj = User.objects.get(username=str(request.POST.get('user')))

        # print('is book obj? ', isinstance(book_obj, Book), '\n\n')
        # print('is user obj? ',isinstance(user_obj, User), '\n\n')

        new_fav = FavoriteBook.objects.create(
            user=user_obj,
            book=book_obj, 
            # session_key=session_key
        )

    return JsonResponse(return_dict)

def check_book_is_favorites(request):
    return_dict = dict()
    session_key = request.session.session_key
    # print("\n\n",request.GET,"\n\n")

    already_exist = FavoriteBook.objects.filter(
        user=request.GET.get('user'), 
        book=request.GET.get('book'), 
        # session_key=session_key
    )

    if already_exist:
        return_dict = {
            'user': request.GET.get('user'),
            'book': request.GET.get('book'), 
            # 'session_key': session_key,
        }

    return JsonResponse(return_dict)

def delete_book_from_favorites(request):
    return_dict = dict()
    session_key = request.session.session_key
    # print("\n\n",request.POST,"\n\n")

    already_exist = FavoriteBook.objects.filter(
        user=request.POST.get('user'), 
        book=request.POST.get('book'), 
        # session_key=session_key
    )

    if already_exist:
        fav = FavoriteBook.objects.get(
            user=request.POST.get('user'), 
            book=request.POST.get('book'), 
            # session_key=session_key
        )
        fav.delete()
        return_dict = {'delete': True}

    return JsonResponse(return_dict)


class PurchasedBooksByUserListView(LoginRequiredMixin, ListView):
    model = PurchasedBook
    template_name = 'catalog/book/book_list_purchased_user.html'

    def get_queryset(self):
        return PurchasedBook.objects.filter(user=self.request.user)

def add_to_purchase(request):
    return_dict = dict()
    session_key = request.session.session_key
    print("\n\nrequest.POST:\n",request.POST,"\n\n")

    already_exist = PurchasedBook.objects.filter(
        user=request.POST.get('user'), 
        book=request.POST.get('book'), 
        # session_key=session_key
    )

    print('ALREADY EXIST:\n', already_exist, '\nis exist?', not already_exist)

    if (not already_exist):
        print('request.POST:\n', request.POST, '\n\n')

        book_obj = Book.objects.get(title=str(request.POST.get('book')))
        user_obj = User.objects.get(username=str(request.POST.get('user')))

        print('is book obj? ', isinstance(book_obj, Book), '\n\n')
        print('is user obj? ',isinstance(user_obj, User), '\n\n')

        new_fav = PurchasedBook.objects.create(
            user=user_obj,
            book=book_obj, 
            # session_key=session_key
        )

    return JsonResponse(return_dict)

def check_purchase(request):
    return_dict = dict()
    session_key = request.session.session_key
    print('\n','='*50,'\n\n','='*50,'\n')
    print('\nCHECK PURCHASE:')
    print("\n\n",request.GET,"\n\n")

    already_exist = PurchasedBook.objects.filter(
        user=request.GET.get('user'), 
        book=request.GET.get('book'), 
        #session_key=session_key
    )

    print('ALREADY EXIST:\n', already_exist)
    print('\n','='*50,'\n\n','='*50,'\n')

    if already_exist:
        return_dict = {
            'user': request.GET.get('user'),
            'book': request.GET.get('book'), 
            # 'session_key': session_key,
        }

    return JsonResponse(return_dict)

def delete_from_purchase(request):
    return_dict = dict()
    session_key = request.session.session_key
    print("\n\n",request.POST,"\n\n")

    already_exist = PurchasedBook.objects.filter(
        user=request.POST.get('user'), 
        book=request.POST.get('book'), 
        # session_key=session_key
    )

    if already_exist:
        fav = PurchasedBook.objects.get(
            user=request.POST.get('user'), 
            book=request.POST.get('book'), 
            # session_key=session_key
        )
        fav.delete()
        return_dict = {'delete': True}

    return JsonResponse(return_dict)


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# Author
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
def authors_list(request):
    search_query = request.GET.get('search', '')

    if (search_query):
        authors = Author.objects.filter(Q(name__icontains=search_query))
    else:
        authors = Author.objects.all()

    return render(request, 'catalog/author/authors_list.html', context={'authors': authors}) 


class AuthorDetailView(ObjectDetailMixin, View):
    model = Author
    template = 'catalog/author/author_detail.html'


class AuthorCreateView(ObjectCreateMixin, View):
    form_model = AuthorForm
    template = 'catalog/author/author_create_form.html'


class AuthorUpdateView(ObjectUpdateMixin, View):
    model = Author
    form_model = AuthorForm
    template = 'catalog/author/author_update_form.html'


class AuthorDeleteView(ObjectDeleteMixin, View):
    model = Author
    template = 'catalog/author/author_delete_form.html'
    redirect_url = 'authors_list_url'


class FavoriteAuthorsByUserListView(LoginRequiredMixin, ListView):
    model = FavoriteAuthor
    template_name = 'catalog/author/authors_favorite_list.html'

    def get_queryset(self):
        return FavoriteAuthor.objects.filter(user=self.request.user)

def add_author_to_favorites(request):
    return_dict = dict()
    session_key = request.session.session_key
    # print("\n\n",request.POST,"\n\n")

    already_exist = FavoriteAuthor.objects.filter(
        user=request.POST.get('user'), 
        author=request.POST.get('author'), 
        # session_key=session_key
    )

    if (not already_exist):
        # print('request.POST:\n', request.POST, '\n\n')

        author_obj = Author.objects.get(name=str(request.POST.get('author')))
        user_obj = User.objects.get(username=str(request.POST.get('user')))

        # print('is author obj? ', isinstance(author_obj, Author), '\n\n')
        # print('is user obj? ',isinstance(user_obj, User), '\n\n')

        new_fav = FavoriteAuthor.objects.create(
            user=user_obj,
            author=author_obj, 
            # session_key=session_key
        )

    return JsonResponse(return_dict)

def check_author_is_favorites(request):
    return_dict = dict()
    session_key = request.session.session_key
    # print("\n\n",request.GET,"\n\n")

    already_exist = FavoriteAuthor.objects.filter(
        user=request.GET.get('user'), 
        author=request.GET.get('author'), 
        # session_key=session_key
    )

    if already_exist:
        return_dict = {
            'user': request.GET.get('user'),
            'author': request.GET.get('author'), 
            # 'session_key': session_key,
        }

    return JsonResponse(return_dict)

def delete_author_from_favorites(request):
    return_dict = dict()
    session_key = request.session.session_key
    # print("\n\n",request.POST,"\n\n")

    already_exist = FavoriteAuthor.objects.filter(
        user=request.POST.get('user'), 
        author=request.POST.get('author'), 
        # session_key=session_key
    )

    if already_exist:
        fav = FavoriteAuthor.objects.get(
            user=request.POST.get('user'), 
            author=request.POST.get('author'), 
            # session_key=session_key
        )
        fav.delete()
        return_dict = {'delete': True}

    return JsonResponse(return_dict)

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# Tag
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
def tags_list(request):
    search_query = request.GET.get('search', '')

    if (search_query):
        tags = Tag.objects.filter(Q(name__icontains=search_query))
    else:
        tags = Tag.objects.all()

    return render(request, 'catalog/tag/tags_list.html', context={'tags': tags})


class TagDetailView(ObjectDetailMixin, View):
    model = Tag
    template = 'catalog/tag/tag_detail.html'


class TagCreateView(ObjectCreateMixin, View):
    form_model = TagForm
    template = 'catalog/tag/tag_create_form.html'


class TagUpdateView(ObjectUpdateMixin, View):
    model = Tag
    form_model = TagForm
    template = 'catalog/tag/tag_update_form.html'


class TagDeleteView(ObjectDeleteMixin, View):
    model = Tag
    template = 'catalog/tag/tag_delete_form.html'
    redirect_url = 'tags_list_url'


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# Quote
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
def quotes_list(request):
    search_query = request.GET.get('search', '')

    if (search_query):
        quotes = Quote.objects.filter(Q(text__icontains=search_query))
    else:
        quotes = Quote.objects.all()

    return render(request, 'catalog/quote/quotes_list.html', context={'quotes': quotes})


class QuoteDetailView(ObjectDetailMixin, View):
    model = Quote
    template = 'catalog/quote/quote_detail.html'


class QuoteCreateView(ObjectCreateMixin, View):
    form_model = QuoteForm
    template = 'catalog/quote/quote_create_form.html'


class QuoteUpdateView(ObjectUpdateMixin, View):
    model = Quote
    form_model = QuoteForm
    template = 'catalog/quote/quote_update_form.html'


class QuoteDeleteView(ObjectDeleteMixin, View):
    model = Quote
    template = 'catalog/quote/quote_delete_form.html'
    redirect_url = 'quotes_list_url'


class FavoriteQuotesByUserListView(LoginRequiredMixin, ListView):
    model = FavoriteQuote
    template_name = 'catalog/quote/quotes_favorite_list.html'

    def get_queryset(self):
        return FavoriteQuote.objects.filter(user=self.request.user)

def add_quote_to_favorites(request):
    return_dict = dict()
    session_key = request.session.session_key
    print("\n\n",request.POST,"\n\n")

    already_exist = FavoriteQuote.objects.filter(
        user=request.POST.get('user'), 
        quote=request.POST.get('quote'), 
        # session_key=session_key
    )

    if (not already_exist):
        print('request.POST:\n', request.POST, '\n\n')

        quote_obj = Quote.objects.get(text=str(request.POST.get('quote')))
        user_obj = User.objects.get(username=str(request.POST.get('user')))

        print('is quote obj? ', isinstance(quote_obj, Quote), '\n\n')
        print('is user obj? ',isinstance(user_obj, User), '\n\n')

        new_fav = FavoriteQuote.objects.create(
            user=user_obj,
            quote=quote_obj, 
            # session_key=session_key
        )

    return JsonResponse(return_dict)

def check_quote_is_favorites(request):
    return_dict = dict()
    session_key = request.session.session_key
    print("\n\n",request.GET,"\n\n")

    already_exist = FavoriteQuote.objects.filter(
        user=request.GET.get('user'), 
        quote=request.GET.get('quote'), 
        # session_key=session_key
    )

    if already_exist:
        return_dict = {
            'user': request.GET.get('user'),
            'quote': request.GET.get('quote'), 
            # 'session_key': session_key,
        }

    return JsonResponse(return_dict)

def delete_quote_from_favorites(request):
    return_dict = dict()
    session_key = request.session.session_key
    print("\n\n",request.POST,"\n\n")

    already_exist = FavoriteQuote.objects.filter(
        user=request.POST.get('user'), 
        quote=request.POST.get('quote'), 
        # session_key=session_key
    )

    if already_exist:
        fav = FavoriteQuote.objects.get(
            user=request.POST.get('user'), 
            quote=request.POST.get('quote'), 
            # session_key=session_key
        )
        fav.delete()
        return_dict = {'delete': True}

    return JsonResponse(return_dict)


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# Buy
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# def buys_list(request):
#     search_query = request.GET.get('search', '')

#     if (search_query):
#         buys = Buy.objects.filter(Q(user__icontains=search_query))
#     else:
#         buys = Buy.objects.all()

#     return render(request, 'catalog/buy/buys_list.html', context={'buys': buys})


# class BuyDetailView(ObjectDetailMixin, View):
#     model = Buy
#     template = 'catalog/buy/buy_detail.html'


# class BuyCreateView(ObjectCreateMixin, View):
#     form_model = BuyForm
#     template = 'catalog/buy/buy_create_form.html'


# class BuyUpdateView(ObjectUpdateMixin, View):
#     model = Buy
#     form_model = BuyForm
#     template = 'catalog/buy/buy_update_form.html'


# class BuyDeleteView(ObjectDeleteMixin, View):
#     model = Buy
#     template = 'catalog/buy/buy_delete_form.html'
#     redirect_url = 'buys_list_url'


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# Coupon
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# def coupons_list(request):
#     search_query = request.GET.get('search', '')

#     if (search_query):
#         coupons = Coupon.objects.filter(Q(name__icontains=search_query))
#     else:
#         coupons = Coupon.objects.all()

#     return render(request, 'catalog/coupon/coupons_list.html', context={'coupons': coupons})


# class CouponDetailView(ObjectDetailMixin, View):
#     model = Coupon
#     template = 'catalog/coupon/coupon_detail.html'


# class CouponCreateView(ObjectCreateMixin, View):
#     form_model = CouponForm
#     template = 'catalog/coupon/coupon_create_form.html'


# class CouponUpdateView(ObjectUpdateMixin, View):
#     model = Coupon
#     form_model = CouponForm
#     template = 'catalog/coupon/coupon_update_form.html'


# class CouponDeleteView(ObjectDeleteMixin, View):
#     model = Coupon
#     template = 'catalog/coupon/coupon_delete_form.html'
#     redirect_url = 'coupons_list_url'


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# Publisher
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# def publishers_list(request):
#     search_query = request.GET.get('search', '')

#     if (search_query):
#         publishers = Publisher.objects.filter(Q(name__icontains=search_query))
#     else:
#         publishers = Publisher.objects.all()

#     return render(request, 'catalog/publisher/publishers_list.html', context={'publishers': publishers})


# class PublisherDetailView(ObjectDetailMixin, View):
#     model = Publisher
#     template = 'catalog/publisher/publisher_detail.html'


# class PublisherCreateView(ObjectCreateMixin, View):
#     form_model = PublisherForm
#     template = 'catalog/publisher/publisher_create_form.html'


# class PublisherUpdateView(ObjectUpdateMixin, View):
#     model = Publisher
#     form_model = PublisherForm
#     template = 'catalog/publisher/publisher_update_form.html'


# class PublisherDeleteView(ObjectDeleteMixin, View):
#     model = Publisher
#     template = 'catalog/publisher/publisher_delete_form.html'
#     redirect_url = 'publishers_list_url'
