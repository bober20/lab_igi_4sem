from django.contrib import admin

import apps.cleaning_service_app.models as m

admin.site.register(m.Employee)
admin.site.register(m.CustomUser)
admin.site.register(m.EmployeePosition)
admin.site.register(m.Client)
admin.site.register(m.Order)
admin.site.register(m.ServiceType)
admin.site.register(m.Service)
admin.site.register(m.News)
admin.site.register(m.Question)
admin.site.register(m.Answer)
admin.site.register(m.Vacancy)
admin.site.register(m.Review)
admin.site.register(m.PromoCode)
admin.site.register(m.Company)
admin.site.register(m.CompanyStory)
admin.site.register(m.Bonus)
