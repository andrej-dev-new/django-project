from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.conf.urls import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('events/', include(('events.urls', 'events'), namespace='events')),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
]

handler404 = 'events.views.custom_404'
handler500 = 'events.views.custom_500'
