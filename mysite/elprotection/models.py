from django.db import models
from datetime import datetime
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
# from django.urls import reverse


class Company(models.Model):
    title = models.CharField(max_length=256, verbose_name='Наименование предприятия')
    slug = models.SlugField(max_length=256, auto_created=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = 'Компании'
        ordering = ['-created']

    def __str__(self):
        return self.title


class Position(models.Model):
    class Category(models.TextChoices):
        WORKER = 'WO', 'Рабочий'
        MANAGER = 'MG', 'Руководитель'
        SPECIALIST = 'SP', 'Специалист'

    title = models.CharField(max_length=256, verbose_name='Название штатной должности')
    company = models.ForeignKey(Company, related_name="positions", on_delete=models.CASCADE)
    category = models.CharField(max_length=2, choices=Category.choices, default=Category.WORKER,
                                verbose_name='Категория должности')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = 'Должности'
        ordering = ['-created']

    def __str__(self):
        return self.title


class Employ(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    number = models.CharField(max_length=8, help_text='Вводите только число', verbose_name='ТабельныйНомер',
                              primary_key=True)
    slug = models.SlugField(max_length=256, auto_created=True)
    surname = models.CharField(max_length=25, blank=True, null=True, verbose_name='Отчество')
    position = models.ForeignKey(Position, related_name='employs', on_delete=models.CASCADE)
    #
    appointed = models.DateTimeField(default=datetime.now, verbose_name='Дата назначения на должность')
    boss = models.ForeignKey('Employ', blank=True, null=True, verbose_name='Начальник', on_delete=models.SET_NULL)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_administrator = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name} {self.surname}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.number)
        return super(Employ, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = 'Сотрудники'


class Admission(models.Model):
    number = models.CharField(max_length=8, help_text='Вводите только числа', verbose_name='id допуска',
                              primary_key=True)
    title = models.CharField(max_length=35, verbose_name="Наименование допуска")
    body = models.TextField(verbose_name='Полное наименование допуска')
    knowledge = models.CharField(max_length=128, verbose_name='Область знаний')
    type = models.CharField(max_length=128, verbose_name='Наименование вида допуска')

    class Meta:
        verbose_name = "Допуск"
        verbose_name_plural = 'Допуска'

    def __str__(self):
        return f"{self.title}"


class Protocol(models.Model):
    class Status(models.TextChoices):
        CLEARED = 'CL', 'Сдал'
        WARNING = 'WR', 'Скоро истечет'
        EXPIRED = 'EX', 'Нет допуска'

    status = models.CharField(max_length=2, choices=Status.choices, default=Status.EXPIRED, verbose_name='Статус',)
    employ = models.ForeignKey(Employ, on_delete=models.CASCADE, verbose_name='Сотрудник')
    admission = models.ForeignKey(Admission, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Допуск')
    start = models.DateTimeField(default=datetime.now, verbose_name='Дата протокола', blank=True, null=True)
    number = models.CharField(max_length=25, verbose_name="Номер протокола", blank=True, null=True)
    end = models.DateTimeField(verbose_name="Дата окончания допуска", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_status(self):
        print(self.end.__str__())
        string_as_date = datetime.strptime(self.end.__str__()[:-6], '%Y-%m-%d %H:%M:%S')
        if (string_as_date < datetime.now()):
            return "Нет допуска"
        else:
            return 'Сдал'


    def get_absolute_url(self):
        pass

    class Meta:
        verbose_name = "Протокол"
        verbose_name_plural = 'Протокола'
