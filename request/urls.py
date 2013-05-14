from django.views.generic import TemplateView
from django.conf.urls import *

urlpatterns = patterns(
    '',
    # Main web portal entrance.
    url(r'^$', TemplateView.as_view(template_name="ticket.html"), name="generator"),
    (r'^api/$', "request.views.ticket"),
    (r'^check/$', "request.views.check"),
)