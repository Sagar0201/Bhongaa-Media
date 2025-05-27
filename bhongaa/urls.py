

from django.urls import path,re_path
from .import views
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # account Urls
    path('', views.home, name="home"),
    path('Login/', views.Login, name="Login"),
    path('SignOut/', views.SignOut, name="SignOut"),
    path('Addpost/', views.addpost, name="Addpost"),
    path('Profile/', views.Profile, name="Profile"),
    path('Messages/', views.Messages, name="Messages"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('search/', views.search, name="search"),
    path('/allposts', views.allposts, name="allposts"),
    path('/post', views.post, name="post"),
    path('/OurClient', views.OurClient, name="OurClient"),

    # for forget password
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="Accounts/reset_password.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="Accounts/password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name="Accounts/password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="Accounts/password_reset_done.html"), name='password_reset_complete'),
    path('change_password/', auth_views.PasswordChangeView.as_view(
        template_name="Accounts/change_password.html"), name='change_password'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(
        template_name="Accounts/password_change_done.html"), name='password_change_done'),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root':settings.STATICFILES_DIRS[0]}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
