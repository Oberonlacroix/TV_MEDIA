
from django.contrib import admin
from django.urls import path, include
from Login.views import home_view
from django.contrib.auth import views as auth_views
from EPG_creation.views import logout_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('EPG_creation/', include('EPG_creation.urls')),
    path('Login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home_view, name='home')
]
