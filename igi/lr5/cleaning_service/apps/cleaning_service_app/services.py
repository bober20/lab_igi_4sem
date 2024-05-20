from datetime import datetime
from statistics import median, mean, mode

from django.db.models import Q, Avg, Max, Count, Sum, Prefetch, ExpressionWrapper, DecimalField, F
from django.db.models import FloatField

import matplotlib.pyplot as plt
import io
import base64
from urllib import parse

from apps.cleaning_service_app.models import Client, ServiceType, Order, Service


def get_orders_sorted_by_clients_and_dates():
    orders_prefetch = Prefetch('order_set', queryset=Order.objects.order_by('date_time'))
    clients_with_order_count = Client.objects.annotate(order_count=Count('order')).prefetch_related(
        orders_prefetch)

    return clients_with_order_count


def client_age_median():
    obj = Client.objects.filter(~Q(user__age=None))
    return median(obj.values_list('user__age', flat=True))


def client_age_mode():
    obj = Client.objects.filter(~Q(user__age=None))
    return mode(obj.values_list('user__age', flat=True))


def client_age_mean():
    obj = Client.objects.filter(~Q(user__age=None))
    return mean(obj.values_list('user__age', flat=True))


def average_service_price():
    price = ServiceType.objects.aggregate(Avg("price", default=0))
    return price["price__avg"]


def get_difference_between_highest_price_and_average():
    difference = ServiceType.objects.aggregate(price_diff=Max("price", output_field=FloatField()) - Avg("price"))
    return difference["price_diff"]


def get_order_with_highest_price():
    orders = Order.objects.all()

    if not orders:
        return None

    orders_with_prices = [(order, order.get_total_price()) for order in orders]
    sorted_orders = sorted(orders_with_prices, key=lambda x: x[1], reverse=True)
    highest_price_order = sorted_orders[0][0] if sorted_orders else None

    return highest_price_order.get_total_price()

    # orders = Order.objects.annotate(
    #     total_price=ExpressionWrapper(
    #         Sum(F('services__service_type__price') * F('services__number')),
    #         output_field=DecimalField()
    #     )
    # ).annotate(
    #     discount=ExpressionWrapper(
    #         F('total_price') * (1 - (F('bonus__discount_percentage') + F('promocode__discount_percentage')) / 100),
    #         output_field=DecimalField()
    #     )
    # ).order_by('-discount')
    #
    # highest_price_order = orders.first()
    #
    # print(highest_price_order.total_price)
    #
    # for order in Order.objects.all():
    #     print(order.get_total_price())

    # orders_prices = Order.objects.aggregate(Max("total_price", default=0))
    # if orders_prices:
    #     return orders_prices['total_price__max']
    # else:
    #     return 0


def plot_service_types():
    service_counts = Service.objects.values('service_type__name').annotate(total=Sum('number'))

    service_types = [sc['service_type__name'] for sc in service_counts]
    counts = [sc['total'] for sc in service_counts]

    plt.figure(figsize=(10, 6))
    plt.bar(service_types, counts)
    plt.xlabel('Service Type')
    plt.ylabel('Number of Services')
    plt.title('Services Types')
    plt.xticks(rotation=45, ha='right')

    for i, count in enumerate(counts):
        plt.text(i, count, str(count), ha='center', va='bottom')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = parse.quote(string)

    return url
