from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="main_page"),
    path('signup/', views.sign_up_form, name="signUp"),
    path('login/', views.login_form, name="login"),
    path('logout/', views.log_out_user, name="logout"),
    path('download/', views.FilterView.as_view(), name="upload"),
    path('multi/', views.UpLoadMultiFile.as_view(), name="multi"),
    path('delete/<name>', views.delete_item, name="delete")

]
