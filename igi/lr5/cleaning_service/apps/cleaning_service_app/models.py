from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUser(AbstractUser):
    age = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(18), MaxValueValidator(100)])
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=13, null=True, default='+375290000000')

    def get_absolute_url_for_delete(self):
        return reverse('users:delete_user', kwargs={'pk': self.pk})

    def get_absolute_url_for_update(self):
        return reverse('users:edit_user', kwargs={'pk': self.pk})

    def __str__(self):
        return self.username


class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    image_source = models.ImageField(upload_to='images/', null=True, blank=True)
    position = models.ForeignKey('EmployeePosition', on_delete=models.SET_NULL, null=True)
    date_of_beginning = models.DateField(auto_now_add=True)
    clients = models.ManyToManyField('Client')

    # def get_absolute_url_for_delete(self):
    #     return reverse('cleaning_service:delete_employee_position', kwargs={'pk': self.pk})

    def __str__(self):
        return self.user.username


class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True)
    legal_entity = models.BooleanField()

    def get_absolute_url(self):
        return reverse('clients', kwargs={'client_id': self.id})

    def __str__(self):
        return self.user.username


class EmployeePosition(models.Model):
    name = models.CharField(max_length=255)
    salary = models.IntegerField()

    def get_absolute_url_for_delete(self):
        return reverse('cleaning_service:delete_employee_position', kwargs={'pk': self.pk})

    def get_absolute_url_for_update(self):
        return reverse('cleaning_service:update_employee_position', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    services = models.ManyToManyField('Service')
    promocode = models.ForeignKey('PromoCode', on_delete=models.SET_NULL, null=True)
    bonus = models.ForeignKey('Bonus', on_delete=models.SET_NULL, null=True)
    # total_price = models.IntegerField()

    class Meta:
        ordering = ["date_time"]
        get_latest_by = "date_tile"

    def get_absolute_url_to_add(self):
        return reverse('cleaning_service:add_service_to_order', kwargs={'pk': self.pk})

    def get_absolute_url_to_more_info(self):
        return reverse('cleaning_service:order_details', kwargs={'pk': self.pk})

    def get_total_price(self):
        total_price = 0

        for service in self.services.all():
            total_price += service.service_type.price * service.number

        total_price *= (100 - (self.bonus.discount_percentage + self.promocode.discount_percentage)) / 100

        return total_price

    def __str__(self):
        return str(self.pk)


class ServiceType(models.Model):
    OFFICE = "OF"
    COTTAGE = "CO"
    FACILITY = "FC"

    SPACE_CHOICES = [
        (OFFICE, 'Office'),
        (COTTAGE, 'Cottage'),
        (FACILITY, 'Facility')
    ]

    name = models.CharField(max_length=2, choices=SPACE_CHOICES, default=FACILITY)
    price = models.IntegerField(null=True, blank=True)
    extra_info = models.TextField(null=True, blank=True)

    def get_absolute_url_for_delete(self):
        return reverse('cleaning_service:delete_service_type', kwargs={'pk': self.pk})

    def get_absolute_url_for_update(self):
        return reverse('cleaning_service:update_service_type', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.name} {self.price} {self.extra_info}'


class Service(models.Model):
    service_type = models.ForeignKey('ServiceType', on_delete=models.CASCADE, null=True)
    number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.service_type.__str__()} {self.number}'


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image_source = models.ImageField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    content = models.TextField()
    date = models.DateTimeField(null=True, blank=True)
    answer = models.ForeignKey('Answer', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.content

    def get_absolute_url_to_add(self):
        return reverse('cleaning_service:add_answer', kwargs={'pk': self.pk})


class Answer(models.Model):
    content = models.TextField()
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.content


class Vacancy(models.Model):
    employee_position = models.ForeignKey('EmployeePosition', on_delete=models.CASCADE)
    number_of_this_position = models.IntegerField()
    vacancy_description = models.TextField()

    def get_absolute_url_for_delete(self):
        return reverse('cleaning_service:delete_vacancy', kwargs={'pk': self.pk})

    def get_absolute_url_for_update(self):
        return reverse('cleaning_service:update_vacancy', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.employee_position.__str__()} {self.number_of_this_position}'


class Review(models.Model):
    author = models.ForeignKey('Client', on_delete=models.CASCADE)
    rate = models.IntegerField()
    content = models.TextField()
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.author.__str__()}'


class PromoCode(models.Model):
    name = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=255)
    discount_percentage = models.IntegerField()

    def __str__(self):
        return self.code


class Bonus(models.Model):
    name = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=255)
    discount_percentage = models.IntegerField()

    def __str__(self):
        return self.code


class Company(models.Model):
    name = models.CharField(max_length=255)
    video = models.FileField(upload_to='images/', null=True, blank=True)
    logo = models.ImageField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class CompanyStory(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
