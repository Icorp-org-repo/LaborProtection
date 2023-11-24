from django.db import models
from datetime import datetime
# from django.urls import reverse


class Company(models.Model):
    name = models.CharField(max_length=128, verbose_name='Наименование предприятия')
    slug = models.SlugField(max_length=256, )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.title


class Employ(models.Model):
    number = models.CharField(max_length=8, help_text='Вводите только число', verbose_name='ТабельныйНомер',
                              primary_key=True)
    second_name = models.CharField(max_length=25, verbose_name="Фамилия")
    name = models.CharField(max_length=25, verbose_name='Имя')
    surname = models.CharField(max_length=25, blank=True, null=True, verbose_name='Отчество')
    position = models.ForeignKey(Position, related_name='employs', on_delete=models.CASCADE)
    #
    appointed = models.DateTimeField(default=datetime.now, verbose_name='Дата назначения на должность')
    boss = models.ForeignKey('Employ', blank=True, null=True, verbose_name='Начальник', on_delete=models.SET_NULL)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.second_name} {self.name} {self.surname}"


class Admission(models.Model):
    number = models.CharField(max_length=8, help_text='Вводите только числа', verbose_name='id допуска',
                              primary_key=True)
    title = models.CharField(max_length=35, verbose_name="Наименование допуска")
    body = models.TextField(verbose_name='Полное наименование допуска')
    knowledge = models.CharField(max_length=128, verbose_name='Область знаний')
    type = models.CharField(max_length=128, verbose_name='Наименование вида допуска')


class Protocol(models.Model):
    class Status(models.TextChoices):
        CLEARED = 'CL', 'Сдал'
        WARNING = 'WR', 'Скоро истечет'
        EXPIRED = 'EX', 'Нет допуска'

    status = models.CharField(max_length=2, choices=Status.choices, default=Status.EXPIRED, verbose_name='Статус')
    employ = models.ForeignKey(Employ, on_delete=models.CASCADE, verbose_name='Сотрудник')
    admission = models.ForeignKey(Admission, blank=True, null=True, on_delete=models.SET_NULL,verbose_name='Допуск')
    start = models.DateTimeField(default=datetime.now, verbose_name='Дата протокола', blank=True, null=True)
    number = models.CharField(max_length=25, verbose_name="Номер протокола", blank=True, null=True)
    end = models.DateTimeField(verbose_name="Дата окончания допуска",blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        pass
