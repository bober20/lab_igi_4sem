# from django.db import models
#
# class CustomUser(AbstractUser):
#     email = models.CharField(max_length=255, null=True, validators=[
#             RegexValidator(
#                 regex=r'\w+@[gmail.com|mail.ru|yandex.ru|bsuir.by]',
#                 message="Enter a valid email."
#             )
#         ]
#     )
#     telephone = models.CharField(max_length=13, null=True, default='+375290000000', validators=[
#             RegexValidator(
#                 regex=r'\+375[0-9][0-9]\d{7}\b',
#                 message="Enter a valid telephone number +375293212345."
#             )
#         ]
#     )
#
#     def __str__(self):
#         return self.username
#
#     list_display = ["first_name", "last_name"]
#
#
# class Employee(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
#     image_source = models.ImageField(upload_to='images/', null=True, blank=True)
#     position = models.ForeignKey('EmployeePosition', on_delete=models.SET_NULL, null=True)
#     date_of_beginning = models.DateField(auto_now_add=True)
#     clients = models.ManyToManyField('Client')
#
#     def get_absolute_url(self):
#         return reverse('employees', kwargs={'employee_id': self.id})
#
#     def __str__(self):
#         return self.user.username
#
#     list_display = ["id", "name", "position"]
#
#
# class Client(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
#     password = models.CharField(max_length=10, null=True)
#     company_name = models.CharField(max_length=255, null=True)
#     legal_entity = models.BooleanField()
#
#     def get_absolute_url(self):
#         return reverse('clients', kwargs={'client_id': self.id})
#
#     def __str__(self):
#         return self.user.username
#
#     list_display = ["first_name", "last_name", "surname"]
