from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.plinterview, name='plinterview'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^signup$', views.signup_view, name='signup'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^vote$', views.form, name='form'),
    url(r'^list$', views.list, name='list'),
    url(r'^get_candidate$', views.get_candidate, name='get_candidate'),
    url(r'^vote/submit$', views.vote, name='vote')
]
