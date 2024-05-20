from datetime import datetime
import calendar
import tzlocal
from django.db.models import Sum
from django.utils.timezone import make_aware
import requests

from apps.cleaning_service_app.models import Order


def get_user_time():
    user_timezone = tzlocal.get_localzone()
    current_date = datetime.now(user_timezone).date()
    current_date_formatted = current_date.strftime("%d/%m/%Y")

    calendar_text = calendar.month(
        datetime.now(user_timezone).year,
        datetime.now(user_timezone).month,
    )

    return {
        "user_timezone": user_timezone,
        "current_date_formatted": current_date_formatted,
        "calendar_text": calendar_text,
    }


def get_monthly_order_total(client):
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    start_date = make_aware(datetime(current_year, current_month, 1))
    if current_month == 12:
        end_date = make_aware(datetime(current_year + 1, 1, 1))
    else:
        end_date = make_aware(datetime(current_year, current_month + 1, 1))

    orders = Order.objects.filter(
        client=client,
        date_time__gte=start_date,
        date_time__lt=end_date
    )

    orders_with_prices = [(order, order.get_total_price()) for order in orders]

    sorted_orders = sorted(orders_with_prices, key=lambda x: x[1], reverse=True)

    total_sum = sum(order.get_total_price() for order in orders)

    # total = Order.objects.filter(
    #     client=client,
    #     date_time__gte=start_date,
    #     date_time__lt=end_date
    # ).aggregate(total_sum=Sum('total_price'))['total_sum']

    return total_sum if total_sum is not None else 0


def upload_employee_file(file):
    with open(f"images/{file.name}", "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

