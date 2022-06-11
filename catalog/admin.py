from re import A
from django.contrib import admin
from .models import *


admin.site.register(Book)
admin.site.register(Author)
admin.site.register(PurchasedBook)
admin.site.register(Tag)
admin.site.register(FavoriteAuthor)
admin.site.register(FavoriteBook)
admin.site.register(Quote)

# admin.site.register(AuthorBook)
# admin.site.register(Publisher)
# admin.site.register(PublisherBook)
# admin.site.register(Buy)
# admin.site.register(BuyComposition)
# admin.site.register(Coupon)
