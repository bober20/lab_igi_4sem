from django.urls import path
import apps.cleaning_service_app.views as views

app_name = 'cleaning_service'

urlpatterns = [
    path('', views.main_page, name='main'),
    path('about_company/', views.about_company_page, name='about_company'),
    path('news/', views.news_page, name='news'),
    path('dictionary/', views.dictionary_page, name='dictionary'),
    path('add_question/', views.AddQuestionView.as_view(), name='add_question'),
    path('add_answer/<int:pk>', views.AddAnswerView.as_view(), name='add_answer'),
    path('contacts/', views.contacts_page, name='contacts'),
    path('privacy/', views.privacy_policy_page, name='privacy_policy'),
    path('vacancy/', views.vacancies_page, name='vacancies'),
    path('disconts/', views.discounts_page, name='discounts'),
    path('reviews/', views.ReviewsView.as_view(), name='reviews'),
    path('services_types/', views.ServicesTypesView.as_view(), name='services_types'),
    path('add_service/', views.AddServiceTypeView.as_view(), name='add_service'),
    path('delete_service_type/<int:pk>', views.delete_service_type, name='delete_service_type'),
    path('update_service_type/<int:pk>', views.update_service_type, name='update_service_type'),
    path('employee_positions/', views.EmployeePositionsView.as_view(), name='employee_positions'),
    path('add_position/', views.AddEmployeePositionView.as_view(), name='add_employee_position'),
    path('delete_position/<int:pk>', views.delete_employee_position, name='delete_employee_position'),
    path('update_position/<int:pk>', views.update_employee_position, name='update_employee_position'),
    path('add_vacancy/', views.AddVacancyView.as_view(), name='add_vacancy'),
    path('delete_vacancy/<int:pk>', views.delete_vacancy, name='delete_vacancy'),
    path('update_vacancy/<int:pk>', views.update_vacancy, name='update_vacancy'),
    path('add_service_to_order/<int:pk>', views.AddServiceView.as_view(), name='add_service_to_order'),
    path('add_order/', views.AddOrderView.as_view(), name='add_order'),
    path('order_details/<int:pk>', views.OrderDetailView.as_view(), name='order_details'),
]