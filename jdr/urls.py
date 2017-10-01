from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^', include('synchro.urls')),
    
    url(r'^admin/', admin.site.urls),

    url(r'^account/login/$', auth_views.login, name='auth-login'),
    url(r'^account/', include('django.contrib.auth.urls'))
]
