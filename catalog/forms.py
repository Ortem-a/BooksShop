from django import forms
from requests import request
from .models import *
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'slug', 'image', 'author', 'description', 'price', 'format', 'writing_date', 'language', 'tag']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            #'image': forms.
            'author': forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'format': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'writing_date': forms.DateInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1'
            }),
            'language': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'tag': forms.CheckboxSelectMultiple(attrs={'class': 'form-check form-check-inline'})
        }

    def clean_slug(self):
        data = self.cleaned_data['slug'].lower()

        if data == 'create':
            raise ValidationError('Slug not may be "Create"')
        # if Book.objects.filter(slug__iexact=data).count():
        #     raise ValidationError(f'Slug must be unique. We already have {data} slug.')

        return data

    def clean_price(self):
        data = self.cleaned_data['price']

        #  Проверка того, что дата не выходит за "нижнюю" границу (не < 0).
        if data < 0:
            raise ValidationError(_('Invalid price - value below 0'))

        # Помните, что всегда надо возвращать "очищенные" данные.
        return data

    def clean_writing_date(self):
        data = self.cleaned_data['writing_date']

        #  Проверка того, что дата написания не в будущем
        if data > datetime.date.today():
            raise ValidationError(_('Invalid date - writing in future'))

        return data


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'slug', 'image', 'date_of_birth', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1'
            }),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        data = self.cleaned_data['slug'].lower()

        if data == 'create':
            raise ValidationError('Slug not may be "Create"')
        if Author.objects.filter(slug__iexact=data).count():
            raise ValidationError(f'Slug must be unique. We already have {data} slug.')

        return data

    def clean_date_of_birth(self):
        data = self.cleaned_data['date_of_birth']

        #  Проверка того, что дата не выходит за "нижнюю" границу (не < 0).
        if data > datetime.date.today():
            raise ValidationError(_('Invalid date - birth in future'))

        # Помните, что всегда надо возвращать "очищенные" данные.
        return data

    def clean_date_of_death(self):
        data = self.cleaned_data['date_of_death']

        #  Проверка того, что дата написания не в будущем
        if data > datetime.date.today():
            raise ValidationError(_('Invalid date - death in future'))

        return data


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'slug', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        data = self.cleaned_data['slug'].lower()

        if data == 'create':
            raise ValidationError('Slug not may be "Create"')
        if Tag.objects.filter(slug__iexact=data).count():
            raise ValidationError(f'Slug must be unique. We already have {data} slug.')

        return data


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'slug', 'author', 'book']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.RadioSelect(attrs={'class': 'form-check'}),
            'book': forms.RadioSelect(attrs={'class': 'form-check'}),
        }

    def clean_slug(self):
        data = self.cleaned_data['slug'].lower()

        if data == 'create':
            raise ValidationError('Slug not may be "Create"')
        if Tag.objects.filter(slug__iexact=data).count():
            raise ValidationError(f'Slug must be unique. We already have {data} slug.')

        return data


# class PublisherForm(forms.ModelForm):
#     class Meta:
#         model = Publisher
#         fields = ['name', 'slug', 'image', 'description']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'slug': forms.TextInput(attrs={'class': 'form-control'}),
#             'description': forms.Textarea(attrs={'class': 'form-control'}),
#         }

#     def clean_slug(self):
#         data = self.cleaned_data['slug'].lower()

#         if data == 'create':
#             raise ValidationError('Slug not may be "Create"')
#         if Tag.objects.filter(slug__iexact=data).count():
#             raise ValidationError(f'Slug must be unique. We already have {data} slug.')

#         return data


# class CouponForm(forms.ModelForm):
#     class Meta:
#         model = Coupon
#         fields = ['name', 'slug', 'description', 'discount']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'slug': forms.TextInput(attrs={'class': 'form-control'}),
#             'description': forms.Textarea(attrs={'class': 'form-control'}),
#             'discount': forms.NumberInput(attrs={'class': 'form-control'}),
#         }

#     def clean_slug(self):
#         data = self.cleaned_data['slug'].lower()

#         if data == 'create':
#             raise ValidationError('Slug not may be "Create"')
#         if Book.objects.filter(slug__iexact=data).count():
#             raise ValidationError(f'Slug must be unique. We already have {data} slug.')

#         return data

#     def clean_discount(self):
#         data = self.cleaned_data['discount']

#         #  Проверка того, что дата не выходит за "нижнюю" границу (не < 0).
#         if data < 0:
#             raise ValidationError(_('Invalid price - value below 0'))

#         if data > 100:
#             raise ValidationError(_('Invalid price - value more than 100'))

#         # Помните, что всегда надо возвращать "очищенные" данные.
#         return data


# class BuyForm(forms.ModelForm):
#     class Meta:
#         model = Buy
#         fields = ['user', 'slug', 'cost', 'date', 'composition']
#         widgets = {
#             #'user': forms.HiddenInput(),
#             'slug': forms.TextInput(attrs={'class': 'form-control'}),
#             'cost': forms.NumberInput(attrs={'class': 'form-control'}),
#             'date': forms.DateInput(attrs={
#                 'class': 'form-control datetimepicker-input',
#                 'data-target': '#datetimepicker1'
#             }),
#             'composition': forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}),
#         }

#     def clean_slug(self):
#         data = self.cleaned_data['slug'].lower()

#         if data == 'create':
#             raise ValidationError('Slug not may be "Create"')
#         if Book.objects.filter(slug__iexact=data).count():
#             raise ValidationError(f'Slug must be unique. We already have {data} slug.')

#         return data

#     def clean_cost(self):
#         data = self.cleaned_data['cost']

#         #  Проверка того, что дата не выходит за "нижнюю" границу (не < 0).
#         if data < 0:
#             raise ValidationError(_('Invalid cost - value below 0'))

#         # Помните, что всегда надо возвращать "очищенные" данные.
#         return data

#     def clean_writing_date(self):
#         data = self.cleaned_data['date']

#         #  Проверка того, что дата написания не в будущем
#         if data > datetime.date.today():
#             raise ValidationError(_('Invalid date - date in future'))

#         return data
