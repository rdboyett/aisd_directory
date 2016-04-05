from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       
    url(r'^admin/', include(admin.site.urls)),
    url(r'^google/', include('google_login.urls')),
    url(r'^badge/', include('badge_app.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



urlpatterns += patterns('directory_app.views',
    (r'^$', 'index'),
    (r'^logoutSuccess/$', 'logoutSuccess'),
    (r'^dashboard/$', 'dashboard'),
    (r'^add/$', 'add'),
    (r'^batch/$', 'batchAdd'),
    (r'^profile/$', 'profile'),
    (r'^myProfile/$', 'myProfile'),
    (r'^searchBar/$', 'search_bar'),
    (r'^search/$', 'searchResults'),
    (r'^editEmployee/(?P<userID>\d+)/$', 'editEmployee'),
    
    
    
    
    (r'^addEmployeeAjax/$', 'addEmployeeAjax'),
    (r'^uploadCSV/$', 'uploadCSV'),
    (r'^getUserInfo/$', 'getUserInfo'),
    (r'^updateEmployee/$', 'updateEmployee'),
    (r'^deleteEmployee/$', 'deleteEmployee'),
    
    
    
    (r'^test/$', 'test'),
)

urlpatterns += patterns('directory_app.extensionViews',
    (r'^login/$', 'login'),
    (r'^search_bar/$', 'search_bar'),
    (r'^extSearch/$', 'search'),
    (r'^submitProfileUpdate/$', 'submitProfileUpdate'),
    (r'^checkSessionLogin/$', 'checkSessionLogin'),
    
)
