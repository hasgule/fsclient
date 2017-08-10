from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_prev$', views.get_prev, name='get_prev'),
    url(r'^signup/$', views.SignUp, name='signup'),
    url(r'^signedup/$', views.signedup, name="signedup"),
    url(r'^sign_out/$', views.sign_out, name="sign_out"),
    url(r'^login/$', views.login_user, name="login_user"),
    url(r'^log__out/$', views.log__out, name="log__out"),
    url(r'^password_reset/$', views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^new_password_form/$', views.new_password_form, name='new_password_form'),
    url(r'^successful_change/$', views.successful_change, name='successful_change' ),
    url(r'^my_profile/$', views.my_profile, name='my_profile'),
    url(r'^users/$', views.my_profile, name='users'),
    url(r'^all_users/$', views.all_users, name='all_users'),
    url(r'^messages/$', views.messages, name='messages'),
    url(r'^message_sent/$', views.message_sent, name='message_sent'),
    url(r'^new_message_page/$', views.new_message_page, name='new_message_page'),
    url(r'^who_displayed', views.who_displayed, name='who_displayed'),
    url(r'^sure_sign_out/$', views.sure_sign_out, name="sure_sign_out"),
    url(r'^venue_details/$', views.venue_details, name="venue_details"),
    url(r'^venue_history_find/$', views.venue_history_find, name="venue_history_find")
]

