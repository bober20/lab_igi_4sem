from datetime import timezone, datetime

from django.db.models import Count, Prefetch
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from apps.cleaning_service_app.apis import *

import apps.cleaning_service_app.models as models
from apps.cleaning_service_app import services
from apps.cleaning_service_app.forms import ReviewForm, ServiceTypeForm, EmployeePositionForm, VacancyForm, OrderForm, \
    ServiceForm, QuestionForm, AnswerForm, SearchForm
import logging

logger = logging.getLogger('django')


class ReviewsView(View):
    template_name = "cleaning_service/reviews.html"
    form_class = ReviewForm

    def get(self, request):
        context = {'reviews': models.Review.objects.all().order_by('-date')}

        if request.user.is_authenticated:
            context['form'] = self.form_class

        return render(request, self.template_name, context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        form = self.form_class(request.POST)
        print(form.data, form.is_valid())
        if form.is_valid():
            review = form.save(commit=False)
            review.author = models.Client.objects.get(user=request.user)
            review.date = datetime.now(timezone.utc)
            review.save()

            logger.info(f'Review was added')

        context = {'reviews': models.Review.objects.all().order_by('-date'), 'form': self.form_class}
        return render(request, self.template_name, context)


class AddOrderView(View):
    template_name = "cleaning_service/add_something.html"
    form_class = OrderForm
    success_url = reverse_lazy('users:client_profile')

    def get(self, request):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        print(form.data)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = models.Client.objects.get(user=request.user)
            # order.date_time = datetime.now(timezone.utc)
            order.save()

            logger.info(f'Order was added')

            return redirect(self.success_url)

        context = {'form': self.form_class}

        logger.info(f'Order was NOT added')

        return render(request, self.template_name, context)


class OrderDetailView(View):
    template_name = "cleaning_service/order_details.html"

    def get(self, request, pk):
        order = models.Order.objects.get(pk=pk)
        services = models.Service.objects.filter(order=order)
        context = {'order': order,
                   'services': services}

        return render(request, self.template_name, context)


class AddServiceView(View):
    template_name = "cleaning_service/add_something.html"
    form_class = ServiceForm
    success_url = reverse_lazy('users:client_profile')

    def get(self, request, pk):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = self.form_class(request.POST)

        if form.is_valid():
            service = models.Service(
                service_type=form.cleaned_data['service_type'],
                number=form.cleaned_data['number'],
            )
            service.save()
            order = models.Order.objects.filter(pk=pk)[0]
            order.services.add(service)
            # order_discount = (100 - (order.discounts.all()[0] + order.bonus.all()[0])) / 100
            # order.total_price += service.number * (service.service_type.price * order_discount)

            order.save()

            logger.info(f'Service was added')

            # order.total_price = order.get_total_price()
            # order.save()
            return redirect(self.success_url)

        logger.info(f'Service was NOT added')

        return render(request, self.template_name, {'form': form})


class AddServiceTypeView(View):
    template_name = "cleaning_service/add_something.html"
    form_class = ServiceTypeForm
    success_url = reverse_lazy('cleaning_service:services_types')

    def get(self, request):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        print(form.data)

        if form.is_valid():
            form.save()

            logger.info(f'Service type was added')

            return redirect(self.success_url)

        logger.info(f'Service type was NOT added')

        return render(request, self.template_name, {'form': form})


def update_service_type(request, pk):
    service_type = models.ServiceType.objects.get(pk=pk)

    if request.method == "GET":
        form = ServiceTypeForm(initial={
            'name': service_type.name,
            'area': service_type.area,
            'price': service_type.price,
        })

        context = {'form': form}
        return render(request, "cleaning_service/add_something.html", context)

    else:
        form = ServiceTypeForm(request.POST)

        if form.is_valid():
            service_type.name = form.cleaned_data['name']
            service_type.area = form.cleaned_data['area']
            service_type.price = form.cleaned_data['price']
            service_type.save()

            logger.info(f'Service type was updated')

            return redirect('cleaning_service:services_types')

        logger.info(f'Service type was NOT updated')

        return render(request, "cleaning_service/add_something.html", {'form': form})


def delete_service_type(request, pk):
    service_type = models.ServiceType.objects.get(pk=pk)
    service_type.delete()

    logger.info(f'Service type was deleted')

    return redirect('cleaning_service:services_types')

# def post_search(request):
#     form = SearchForm()
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             cd = form.cleaned_data
#             results = SearchQuerySet().models(models.ServiceType).filter(content=cd['query']).load_all()
#             # count total results
#             total_results = results.count()
#     return render(request,
#                   'blog/post/search.html',
#                   {'form': form,
#                    'cd': cd,
#                    'results': results,
#                    'total_results': total_results})


class ServicesTypesView(View):
    template_name = "cleaning_service/services.html"
    form = SearchForm

    def get(self, request):
        context = {'service_types': models.ServiceType.objects.all().order_by('-price'), 'form': self.form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            service_types = models.ServiceType.objects.filter(name=cd['query']).order_by('-price')
            total_results = service_types.count()
            return render(request,
                              self.template_name,
                              {'form': form,
                               'service_types': service_types,
                               'total_results': total_results})



class AddEmployeePositionView(View):
    template_name = "cleaning_service/add_something.html"
    form_class = EmployeePositionForm
    success_url = reverse_lazy('cleaning_service:employee_positions')

    def get(self, request):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            logger.info(f'Employee position was added')

            return redirect(self.success_url)

        logger.info(f'Employee position was NOT added')

        return render(request, self.template_name, {'form': form})


def update_employee_position(request, pk):
    employee_position = models.EmployeePosition.objects.get(pk=pk)

    if request.method == "GET":
        form = EmployeePositionForm(initial={
            'name': employee_position.name,
            'area': employee_position.salary,
        })

        context = {'form': form}
        return render(request, "cleaning_service/add_something.html", context)

    else:
        form = EmployeePositionForm(request.POST)

        if form.is_valid():
            employee_position.name = form.cleaned_data['name']
            employee_position.salary = form.cleaned_data['salary']
            employee_position.save()

            logger.info(f'Employee position was updated')

            return redirect('cleaning_service:employee_positions')

        logger.info(f'Employee position was NOT updated')

        return render(request, "cleaning_service/add_something.html", {'form': form})


def delete_employee_position(request, pk):
    employee_position = models.EmployeePosition.objects.get(pk=pk)
    employee_position.delete()

    logger.info(f'Employee position was deleted')

    return redirect('cleaning_service:employee_positions')


class EmployeePositionsView(View):
    template_name = "cleaning_service/employee_positions.html"

    def get(self, request):
        logger.info(f'Employee positions view was accessed')

        context = {'employee_positions': models.EmployeePosition.objects.all()}
        return render(request, self.template_name, context)


class AddVacancyView(View):
    template_name = "cleaning_service/add_something.html"
    form_class = VacancyForm
    success_url = reverse_lazy('cleaning_service:vacancies')

    def get(self, request):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            logger.info(f'Vacancy was added')

            return redirect(self.success_url)

        logger.info(f'Vacancy was not added')

        return render(request, self.template_name, {'form': form})


class AddQuestionView(View):
    template_name = "cleaning_service/add_something.html"
    success_url = reverse_lazy('cleaning_service:dictionary')
    form_class = QuestionForm

    def get(self, request):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.date = datetime.now()
            question.save()

            logger.info(f'Question was added {question.pk}')

            return redirect(self.success_url)

        logger.info(f'Question was NOT added')

        return render(request, self.template_name, {'form': form})


class AddAnswerView(View):
    template_name = "cleaning_service/add_something.html"
    success_url = reverse_lazy('cleaning_service:dictionary')
    form_class = AnswerForm

    def get(self, request, pk):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = self.form_class(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.date = datetime.now()
            answer.save()
            question = models.Question.objects.get(pk=pk)
            question.answer = answer
            question.save()

            logger.info(f'Answer was added to question {question.pk}')

            return redirect(self.success_url)

        logger.info(f'Answer was NOT added to question')

        return render(request, self.template_name, {'form': form})


def update_vacancy(request, pk):
    logger.info('Update vacancy view was accessed')

    vacancy = models.Vacancy.objects.get(pk=pk)

    if request.method == "GET":
        form = VacancyForm(initial={
            'employee_position': vacancy.employee_position,
            'number_of_this_position': vacancy.number_of_this_position,
            'vacancy_description': vacancy.vacancy_description,
        })

        context = {'form': form}
        return render(request, "cleaning_service/add_something.html", context)

    else:
        form = VacancyForm(request.POST)

        if form.is_valid():
            vacancy.employee_position = form.cleaned_data['employee_position']
            vacancy.number_of_this_position = form.cleaned_data['number_of_this_position']
            vacancy.vacancy_description = form.cleaned_data['vacancy_description']
            vacancy.save()

            logger.info(f'Vacancy where pk={pk} was updated')

            return redirect('cleaning_service:vacancies')

        logger.info('Vacancy where pk={pk} was NOT updated')

        return render(request, "cleaning_service/add_something.html", {'form': form})


def delete_vacancy(request, pk):
    vacancy = models.Vacancy.objects.get(pk=pk)
    vacancy.delete()

    logger.info(f'Vacancy was deleted')
    return redirect('cleaning_service:vacancies')


def main_page(request):
    logger.info('Main view was accessed')

    latest_news = models.News.objects.order_by('-date').first()

    context = {
        "latest_news": latest_news,
        "cat_facts": get_cat_facts()["fact"],
        "bitcoin_price": get_current_bitcoin_price()
    }

    return render(request, "cleaning_service/main.html", context)


def news_page(request):
    logger.info('News view was accessed')

    news = models.News.objects.order_by('-date')

    context = {"news": news}

    return render(request, "cleaning_service/news.html", context)


def about_company_page(request):
    logger.info('About company view was accessed')

    stories = models.CompanyStory.objects.all()
    company = models.Company.objects.all()

    context = {"stories": stories,
               'client_age_median': services.client_age_median(),
               'client_age_mean': services.client_age_mean(),
               'client_age_mode': services.client_age_mode(),
               'average_service_price': services.average_service_price(),
               'get_difference_between_highest_price_and_average': services.get_difference_between_highest_price_and_average(),
               'get_order_with_highest_price': services.get_order_with_highest_price(),
               'histogram_url': services.plot_service_types(),
               'clients_with_order_count': services.get_orders_sorted_by_clients_and_dates(),
               'company': company}

    # Print clients and their orders
    # for client in clients_with_order_count:
    #     print(f"Client: {client.user.email} - Number of Orders: {client.order_count}")
    #     for order in client.order_set.all():
    #         print(f"Order ID: {order.id}")

    return render(request, "cleaning_service/about_company.html", context)


def dictionary_page(request):
    logger.info('Dictionary view was accessed')

    questions = models.Question.objects.all().order_by('-date')

    context = {"questions": questions}

    return render(request, "cleaning_service/dictionary.html", context)


def contacts_page(request):
    logger.info('Contacts view was accessed')

    employees = models.Employee.objects.all()

    context = {"employees": employees}

    return render(request, "cleaning_service/contact_info.html", context)


def privacy_policy_page(request):
    logger.info('Privacy policy view was accessed')

    return render(request, "cleaning_service/privacy_policy.html")


def vacancies_page(request):
    logger.info('Vacancies view was accessed')

    vacancies = models.Vacancy.objects.all()

    context = {"vacancies": vacancies}

    return render(request, "cleaning_service/vacancies.html", context)


def discounts_page(request):
    logger.info('Discounts view was accessed')

    promo_codes = models.PromoCode.objects.all()
    bonuses = models.Bonus.objects.all()
    context = {"promo_codes": promo_codes, "bonuses": bonuses}

    return render(request, "cleaning_service/discounts.html", context)



