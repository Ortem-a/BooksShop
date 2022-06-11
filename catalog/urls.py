from xml.etree.ElementInclude import include
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
]

urlpatterns += [
    path('register/', views.MyRegisterFormView.as_view(), name='register_url'),
]

urlpatterns += [
    path('books/', views.books_list, name='books_list_url'),
    path('book/create/', views.BookCreateView.as_view(), name='book_create_form_url'),
    path('book/<str:slug>', views.BookDetailView.as_view(), name='book_detail_url'),
    path('book/<str:slug>/update', views.BookUpdateView.as_view(), name='book_update_url'),
    path('book/<str:slug>/delete', views.BookDeleteView.as_view(), name='book_delete_url'),

    path('books/favorite_books/', views.FavoriteBooksByUserListView.as_view(), name='books_favorite_list_url'),
    path('book/add_book_to_favorites/', views.add_book_to_favorites, name='add_book_to_favorites_url'),
    path('book/check_book_is_favorites/', views.check_book_is_favorites, name='check_book_is_favorites_url'),
    path('book/delete_book_from_favorites/', views.delete_book_from_favorites, name='delete_book_from_favorites_url'),

    path('books/mybooks', views.PurchasedBooksByUserListView.as_view(), name='books_purchased_list_url'),
    path('book/add_to_purchase/', views.add_to_purchase, name='add_to_purchase_url'),
    path('book/check_purchase/', views.check_purchase, name='check_purchase_url'),
    path('book/delete_from_purchase/', views.delete_from_purchase, name='delete_from_purchase_url'),
]

urlpatterns += [
    path('authors/', views.authors_list, name='authors_list_url'),
    path('author/create/', views.AuthorCreateView.as_view(), name='author_create_form_url'),
    path('author/<str:slug>', views.AuthorDetailView.as_view(), name='author_detail_url'),
    path('author/<str:slug>/update', views.AuthorUpdateView.as_view(), name='author_update_url'),
    path('author/<str:slug>/delete', views.AuthorDeleteView.as_view(), name='author_delete_url'),

    path('authors/favorite_authors/', views.FavoriteAuthorsByUserListView.as_view(), name='authors_favorite_list_url'),
    path('author/add_author_to_favorites/', views.add_author_to_favorites, name='add_author_to_favorites_url'),
    path('author/check_author_is_favorites/', views.check_author_is_favorites, name='check_author_is_favorites_url'),
    path('author/delete_author_from_favorites/', views.delete_author_from_favorites, name='delete_author_from_favorites_url'),
]

urlpatterns += [
    path('tags/', views.tags_list, name='tags_list_url'),
    path('tag/create/', views.TagCreateView.as_view(), name='tag_create_form_url'),
    path('tag/<str:slug>', views.TagDetailView.as_view(), name='tag_detail_url'),
    path('tag/<str:slug>/update', views.TagUpdateView.as_view(), name='tag_update_url'),
    path('tag/<str:slug>/delete', views.TagDeleteView.as_view(), name='tag_delete_url'),
]

urlpatterns += [
    path('quotes/', views.quotes_list, name='quotes_list_url'),
    path('quote/create/', views.QuoteCreateView.as_view(), name='quote_create_form_url'),
    path('quote/<str:slug>', views.QuoteDetailView.as_view(), name='quote_detail_url'),
    path('quote/<str:slug>/update', views.QuoteUpdateView.as_view(), name='quote_update_url'),
    path('quote/<str:slug>/delete', views.QuoteDeleteView.as_view(), name='quote_delete_url'),

    path('quotes/favorite_quotes/', views.FavoriteQuotesByUserListView.as_view(), name='quotes_favorite_list_url'),
    path('quote/add_quote_to_favorites/', views.add_quote_to_favorites, name='add_quote_to_favorites_url'),
    path('quote/check_quote_is_favorites/', views.check_quote_is_favorites, name='check_quote_is_favorites_url'),
    path('quote/delete_quote_from_favorites/', views.delete_quote_from_favorites, name='delete_quote_from_favorites_url'),
]

# urlpatterns += [
#     path('buys/', views.buys_list, name='buys_list_url'),
#     path('buy/create/', views.BuyCreateView.as_view(), name='buy_create_form_url'),
#     #path('buy/create/', views.buy_create_view, name='buy_create_form_url'),
#     path('buy/<str:slug>', views.BuyDetailView.as_view(), name='buy_detail_url'),
#     path('buy/<str:slug>/update', views.BuyUpdateView.as_view(), name='buy_update_url'),
#     path('buy/<str:slug>/delete', views.BuyDeleteView.as_view(), name='buy_delete_url'),
# ]

# urlpatterns += [
#     path('coupons/', views.coupons_list, name='coupons_list_url'),
#     path('coupon/create/', views.CouponCreateView.as_view(), name='coupon_create_form_url'),
#     path('coupon/<str:slug>', views.CouponDetailView.as_view(), name='coupon_detail_url'),
#     path('coupon/<str:slug>/update', views.CouponUpdateView.as_view(), name='coupon_update_url'),
#     path('coupon/<str:slug>/delete', views.CouponDeleteView.as_view(), name='coupon_delete_url'),
# ]

# urlpatterns += [
#     path('publishers/', views.publishers_list, name='publishers_list_url'),
#     path('publisher/create/', views.PublisherCreateView.as_view(), name='publisher_create_form_url'),
#     path('publisher/<str:slug>', views.PublisherDetailView.as_view(), name='publisher_detail_url'),
#     path('publisher/<str:slug>/update', views.PublisherUpdateView.as_view(), name='publisher_update_url'),
#     path('publisher/<str:slug>/delete', views.PublisherDeleteView.as_view(), name='publisher_delete_url'),
# ]
