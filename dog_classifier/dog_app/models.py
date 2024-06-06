from django.db import models
from django.db.models import Q
from django.urls import reverse


# Create your models here.
class Dog(models.Model):
    class Genders(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'

    name = models.CharField(max_length=100, verbose_name='Кличка')
    age = models.IntegerField(verbose_name='Возраст')
    breed = models.ForeignKey('Breed', on_delete=models.RESTRICT, verbose_name='Порода')
    gender = models.CharField(max_length=1, choices=Genders, verbose_name='Пол')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    favorite_food = models.CharField(max_length=100, verbose_name='Любимая еда')
    favorite_toy = models.CharField(max_length=100, verbose_name='Любимая игрушка')

    class Meta:
        verbose_name = "Собака"
        verbose_name_plural = 'Собаки'
        constraints = [
            models.CheckConstraint(check=Q(age__gte=0), name='age_check'),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dog_detail_view', kwargs={'pk': self.pk})


class Breed(models.Model):
    class Genders(models.TextChoices):
        TINY = 'Tiny'
        SMALL = 'Small'
        MEDIUM = 'Medium'
        LARGE = 'Large'

    name = models.CharField(max_length=100, verbose_name='Название')
    size = models.CharField(choices=Genders, verbose_name='Размер')
    friendliness = models.IntegerField(verbose_name='Дружелюбность')
    trainability = models.IntegerField(verbose_name='Тренируемость')
    shedding_amount = models.IntegerField(verbose_name='Количество линек')
    exercise_needs = models.IntegerField(verbose_name='Потребность в упражнениях')

    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = 'Породы'
        constraints = [
            models.CheckConstraint(check=Q(friendliness__gte=1) & Q(friendliness__lte=5),
                                   name='friendliness_check'),
            models.CheckConstraint(check=Q(trainability__gte=1) & Q(trainability__lte=5),
                                   name='trainability_check'),
            models.CheckConstraint(check=Q(shedding_amount__gte=1) & Q(shedding_amount__lte=5),
                                   name='shedding_amount_check'),
            models.CheckConstraint(check=Q(exercise_needs__gte=1) & Q(exercise_needs__lte=5),
                                   name='exercise_needs_check'),
        ]

    def __str__(self):
        return self.name
