from django.contrib import admin
from django.urls import path
from bhav import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Show_data),
    # path('savedata/', views.background_task, name="savedata"),
    path('search/', views.search_data, name="search"),
]
