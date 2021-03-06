"""sfr_viewer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from costcompare import views as ccviews
from alignments import views as alviews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', ccviews.index, name='index'),
    # url(r'^alignments/(?P<alignment>[^\.]+)', alviews.index, name='align_detail'),
    # url(r'^compare/(?P<alignmenta>[^\.]+)/(?P<alignmentb>[^\.]+)/$',
    #     alviews.compare, name='align_compare'),
    #
    # url(r'^phase/(?P<alignmenta>[^\.]+)/(?P<alignmentb>[^\.]+)/$',
    #     alviews.phase_view, name='phase_compare'),
    url(r'^dashboard/(?P<phase_slug>[^\.]+)/',
        alviews.dashboard, name='dashboard'),
    
    url(r'^pennsport/(?P<phase_slug>[^\.]+)/',
        alviews.mapbox_view, name='mapbox_compare'),
]
