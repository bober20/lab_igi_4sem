from datetime import datetime

from django import forms

from apps.cleaning_service_app.models import Review, Order, Employee, ServiceType, EmployeePosition, Vacancy, Service, \
    Question, Answer
from apps.users_app.custom_mixins import ValidationMixin


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['author', 'date']


class ServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceType
        exclude = []


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ['']


class OrderForm(forms.ModelForm):
    date_time = forms.DateTimeField(
        required=True,
        input_formats=["%d/%m/%y %H:%M"],
        widget=forms.DateTimeInput(format="%d/%m/%y %H:%M")
    )

    class Meta:
        model = Order
        exclude = ['client', 'services']


class EmployeePositionForm(forms.ModelForm):
    class Meta:
        model = EmployeePosition
        exclude = []


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = []


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['date', 'answer']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ['date']


class SearchForm(forms.Form):
    query = forms.CharField()


# class ServiceTypeForm(forms.ModelForm):
#     service = forms.ModelChoiceField(queryset=ServiceType.objects.all(), widget=forms.ChoiceField)
#     employee = forms.ModelChoiceField(queryset=Employee.objects.all(), widget=forms.ChoiceField)
#
#     class Meta:
#         model = ServiceType
#         exclude = ['']



# class OrderForm(forms.ModelForm):
#     service = forms.ModelMultipleChoiceField(queryset=ServiceType.objects.all(), widget=forms.CheckboxSelectMultiple)
#
#     class Meta:
#         model = Order
#         exclude = ['client', ]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields.update(ServiceForm().fields)



