import datetime

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth.hashers import make_password
from tzlocal import get_localzone

from .forms import LoginForm, UserRegistrationForm, ClientRegistrationForm, EmployeeRegistrationForm
import apps.cleaning_service_app.models as models

from .services import get_user_time, get_monthly_order_total, upload_employee_file
import tzlocal
import calendar
import logging
from django.utils import timezone

logger = logging.getLogger('django')


class LoginView(View):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('cleaning_service:main')

    def get(self, request):
        print("users", models.CustomUser.objects.all())
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])

            if user:
                login(request, user)

                logger.info(f'User logged in')

                return redirect(self.success_url)

        logger.info(f'User didn\'t log in')

        return render(request, self.template_name, {'form': form})


class ClientRegistrationView(View):
    template_name = 'users/registration.html'
    form_class = ClientRegistrationForm
    success_url = reverse_lazy('users:login')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        client = self.form_class(request.POST)
        if client.is_valid():
            data = client.cleaned_data

            user = models.CustomUser(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=make_password(data['password1']),
                telephone=data['telephone'],
                username=data['email'],
                age=data['age'],
            )
            print("result: ", user, user.save())

            client_object = client.save(commit=False)
            client_object.user = user
            client_object.save()

            logger.info(f'Client was added')

            return redirect('users:login')

        logger.info(f'Client was NOT added')

        return render(request, self.template_name, {'form': client})


class EmployeeRegistrationView(View):
    template_name = 'users/registration.html'
    form_class = EmployeeRegistrationForm
    success_url = reverse_lazy('users:employees')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        employee = self.form_class(request.POST, request.FILES)
        if employee.is_valid():
            data = employee.cleaned_data

            user = models.CustomUser(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=make_password(data['password1']),
                telephone=data['telephone'],
                username=data['email'],
                age=data['age'],
                is_staff=True,
            )
            user.save()
            employee_object = employee.save(commit=False)
            employee_object.user = user
            employee_object.image_source = data['image_source']
            employee_object.date_of_beginning = datetime.datetime.now()
            employee_object.save()
            employee_object.clients.set(data['clients'])
            employee_object.save()

            logger.info(f'Employee was added')

            return redirect('users:employees')

        logger.info(f'Employee was NOT added')

        return render(request, self.template_name, {'form': employee})


def delete_user(request, pk):
    user = models.CustomUser.objects.get(pk=pk)

    user.delete()

    logger.info(f'User was deleted')

    return redirect('cleaning_service:main')


def edit_employee(request, pk):
    custom_user = models.CustomUser.objects.get(pk=pk)
    employee = models.Employee.objects.get(user=custom_user)
    form = EmployeeRegistrationForm({
        'first_name': custom_user.first_name,
        'last_name': custom_user.last_name,
        'email': custom_user.email,
        'telephone': custom_user.telephone,
        'age': custom_user.age,
        'image_source': employee.image_source,
        'clients': employee.clients.all(),
        'position': employee.position,
    })

    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            custom_user.first_name = data['first_name']
            custom_user.last_name = data['last_name']
            custom_user.email = data['email']
            custom_user.password = make_password(data['password1'])
            custom_user.telephone = data['telephone']
            custom_user.username = data['email']
            custom_user.age = data['age']

            custom_user.save()

            employee.image_source = data['image_source']
            employee.position = data['position']
            employee.clients.set(data['clients'])
            employee.save()

            logger.info(f'Employee was edited')

            return redirect('users:employees')

    return render(request, 'users/registration.html', {'form': form})


class ProfileClientView(View):
    template_name = 'users/profile.html'
    context = 0

    def get(self, request):
        current_user = models.Client.objects.get(user=request.user)
        orders = sorted(models.Order.objects.filter(client=current_user), key=lambda o: o.date_time)

        monthly_statistics = get_monthly_order_total(current_user)

        tz = tzlocal.get_localzone()
        local_time = timezone.localtime(timezone.now())
        utc_time = timezone.now().strftime('%d-%m-%Y %H:%M:%S')

        text_cal = calendar.month(local_time.year, local_time.month)

        self.context = {
            'current_user': current_user,
            'orders': orders,
            'user_timezone': tz,
            'current_date_formatted': local_time,
            'calendar_text': text_cal,
            'utc_time': utc_time,
            'monthly_statistics': monthly_statistics,
        }

        return render(request, self.template_name, self.context)


class ProfileEmployeeView(View):
    template_name = 'users/profile.html'

    def get(self, request):
        current_user = models.Employee.objects.get(user=request.user)
        clients = sorted(current_user.clients.all(), key=lambda x: x.user.last_name)
        tz = tzlocal.get_localzone()
        local_time = timezone.localtime(timezone.now())
        utc_time = timezone.now().strftime('%d-%m-%Y %H:%M:%S')
        text_cal = calendar.month(local_time.year, local_time.month)
        orders_by_client = {}
        for client in clients:
            orders_by_client[client] = models.Order.objects.filter(client=client)



        context = {
            'current_user': current_user,
            'clients': clients,
            'user_timezone': tz,
            'current_date_formatted': local_time,
            'calendar_text': text_cal,
            'utc_time': utc_time,
            'orders_by_client': orders_by_client,
        }
        # for order in orders_by_client:
        #     print(order.client)

        return render(request, self.template_name, context)


class EmployeesView(View):
    template_name = "users/employees.html"

    def get(self, request):
        context = {'employees': models.Employee.objects.all()}
        return render(request, self.template_name, context)


class ClientsView(View):
    template_name = "users/clients.html"

    def get(self, request):
        context = {'clients': models.Client.objects.all()}
        return render(request, self.template_name, context)


class LogoutView(View):
    success_url = reverse_lazy('users:login')

    def get(self, request):
        logout(request)

        logger.info(f'User logged out')

        return redirect(self.success_url)


# class AddServiceTypeView(View):
#     template_name = "cleaning_service/add_something.html"
#     form_class = ServiceTypeForm
#     success_url = reverse_lazy('cleaning_service:services_types')
#
#     def get(self, request):
#         context = {'form': self.form_class}
#         return render(request, self.template_name, context)
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#
#         if form.is_valid():
#             form.save()
#             return redirect(self.success_url)
#
#         return render(request, self.template_name, {'form': form})
#
#
# def update_service_type(request, pk):
#     service_type = models.ServiceType.objects.get(pk=pk)
#
#     if request.method == "GET":
#         form = ServiceTypeForm(initial={
#             'name': service_type.name,
#             'area': service_type.area,
#             'price': service_type.price,
#         })
#
#         context = {'form': form}
#         return render(request, "cleaning_service/add_something.html", context)
#
#     else:
#         form = ServiceTypeForm(request.POST)
#
#         if form.is_valid():
#             service_type.name = form.cleaned_data['name']
#             service_type.area = form.cleaned_data['area']
#             service_type.price = form.cleaned_data['price']
#             service_type.save()
#             return redirect('cleaning_service:services_types')
#
#         return render(request, "cleaning_service/add_something.html", {'form': form})
#
#
# def delete_service_type(request, pk):
#     service_type = models.ServiceType.objects.get(pk=pk)
#     service_type.delete()
#     return redirect('cleaning_service:services_types')
#
#

#



# def register_user(request):
#     if request.method == 'POST':
#         client = ClientRegistrationForm(request.POST)
#
#         if client.is_valid():
#             client.save()
#             return redirect("users:login")
#
#     client = ClientRegistrationForm()
#     context = {
#         "client": client,
#     }
#
#     return render(request, "users/registration.html", context)


# def login_user(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 return redirect('cleaning_service:main')
#     else:
#         form = LoginForm()
#
#     return render(request, 'users/login.html', {'form': form})


# def logout_user(request):
#     logout(request)
#     return redirect('users:login')
