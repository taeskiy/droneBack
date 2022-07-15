from ckeditor.fields import RichTextField
from django.db import models


class Banner(models.Model):
    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'
        ordering = ['-id']

    image = models.ImageField('Картинка')
    url = models.URLField('Ссылка', null=True, default=None, blank=True)

    def __str__(self):
        return self.url if self.url else str(self.pk)


class MainCollections(models.Model):
    class Meta:
        verbose_name = 'Коллекция на главной'
        verbose_name_plural = 'Коллекции на главной'

    title = models.CharField('Название', max_length=128)
    category = models.ForeignKey('category.Category', models.PROTECT)

    def __str__(self):
        return self.title


class CollectionProducts(models.Model):
    class Meta:
        verbose_name = 'Коллекция на главной'
        verbose_name_plural = 'Коллекции на главной'

    collection = models.ForeignKey('MainCollections', models.CASCADE, related_name='products')
    product = models.ForeignKey('product.Product', models.CASCADE, related_name='collection_product')

    def __str__(self):
        return f'{self.collection} | {self.product}'


class Faq(models.Model):
    question = models.TextField()
    answer = RichTextField()
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        verbose_name = 'Вопросы ответы'
        verbose_name_plural = 'Вопросы ответы'
        ordering = ['my_order']

    def __str__(self):
        return self.question
