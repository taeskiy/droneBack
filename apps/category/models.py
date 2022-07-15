import uuid
from django.db import models
from django.utils.text import slugify
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from unidecode import unidecode


class Category(MPTTModel):
    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = "Категория"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    title = models.CharField('Название', max_length=128)
    image = models.ImageField('Изображение', blank=True, null=True)
    icon = models.FileField('Иконка', blank=True, null=True)
    parent = TreeForeignKey('self', verbose_name='Родительская категория', blank=True, null=True,
                            related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.parent.title if self.parent else ""}'

    def save(self, *args, **kwargs):
        if not bool(self.slug):
            new_slug = slugify(unidecode(self.title), allow_unicode=True)
            if Category.objects.filter(slug=new_slug).exists():
                new_slug += str(self.id)
            self.slug = new_slug
        super().save(*args, **kwargs)
