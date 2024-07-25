
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('accounts.urls')),
    path('boards/',include('work_entry_app.urls')),
]
