from django import forms

from dog_app.models import Dog, Breed


class DogAddForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label='Кличка')
    age = forms.IntegerField(label='Возраст')
    gender = forms.ChoiceField(choices=(('M', 'Мужчина'),
                                        ('F', 'Женщина')), label='Пол')
    breed = forms.ModelChoiceField(queryset=Breed.objects.all(), label='Порода')
    color = forms.CharField(max_length=50, label='Цвет')
    favorite_food = forms.CharField(max_length=100, label='Любимая еда')
    favorite_toy = forms.CharField(max_length=100, label='Любимая игрушка')

    class Meta:
        model = Dog
        fields = '__all__'

