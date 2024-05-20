from django.urls import path
import apps.users_app.views as views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('registration/', views.ClientRegistrationView.as_view(), name='registration'),
    path('add_employee/', views.EmployeeRegistrationView.as_view(), name='add_employee'),
    path('delete_user/<int:pk>', views.delete_user, name='delete_user'),
    path('edit_user/<int:pk>', views.edit_employee, name='edit_user'),
    path('employees/', views.EmployeesView.as_view(), name='employees'),
    path('clients/', views.ClientsView.as_view(), name='clients'),
    path('employee_profile/', views.ProfileEmployeeView.as_view(), name='employee_profile'),
    path('client_profile/', views.ProfileClientView.as_view(), name='client_profile'),
]