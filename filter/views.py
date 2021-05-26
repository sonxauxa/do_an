import os
import subprocess
import time

import numpy as np
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, HttpResponse
from django.views import generic
from django.views.generic.edit import FormView

from .decorators import authenticated_user
from .forms import CreateUserForm, UpLoad
from .models import FileFormUpLoad
from .models import Pelcon

LOGIN_URL = 'your_url'
BASE_DIR1 = '/home/s/Desktop/djangoProject1/document/'
BASE_DIR = '/home/s/Desktop/djangoProject1/store/'
BASE_DIR2 = '/home/s/Desktop/djangoProject1/store/filter_file/'
DOC_FILTER = '/home/s/Desktop/DocBleach-master/cli/target/docbleach.jar'
FILTER_DIR = '/home/s/Desktop/djangoProject1/store/pdfs'


def main_page(request):
    return render(request, 'index.html')


def home_page(request):
    return render(request, 'home.html')


@authenticated_user
def sign_up_form(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = UserCreationForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Successful create new account" + user)
                return redirect('login')
        context = {'form': form}
        return render(request, 'register.html', context)


@authenticated_user
def login_form(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username', )
            password = request.POST.get('password', )
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'username or password is incorrect')
    context = {}
    return render(request, 'login.html', context)


def log_out_user(request):
    logout(request)
    return redirect('/login/')


# class UpdateMulti(LoginRequiredMixin, FormView):
#     login_url = '/login/'
#     redirect_field_name = 'redirect_to'
#     form_class = UpLoad
#     template_name = 'upload1.html'  # Replace with your template.
#     success_url = '/'  # Replace with your URL or reverse().
#     mess = ""
#
#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         files = request.FILES.getlist('file_field')
#         if form.is_valid():
#             for f in files:
#                 instance = FileFormUpLoad(file=f, owner=self.request.user.id)
# #                 instance.save()
#                 # os.mkdir('/home/s/Desktop/djangoProject1/store/' + str(self.request.user.id))
#                 subprocess.run('python2 /home/s/Desktop/exefilter/ExeFilter.py /home/s/Desktop/djangoProject1/document/' + f.name + ' ' + '-d' + ' ' + '/home/s/Desktop/djangoProject1/store/pdfs', shell=True)
#                 # subprocess.run(
#                 # 'java -jar /home/s/Desktop/DocBleach-master/cli/target/docbleach.jar -in /home/s/Desktop/djangoProject1/document/' + f.name + ' ' + '-out /home/s/Desktop/djangoProject1/store/pdfs/' + f.name, shell=True)
#             for file_name in os.listdir('/home/s/Desktop/djangoProject1/store/pdfs'):
#                 a = Pelcon(pdf=file_name, owner=self.request.user.id, name=file_name)
#                 a.user = request.user
#                 a.save()
#
#             # path = '/home/s/Desktop/djangoProject1/document'
#             time.sleep(0.5)
#             for f in os.listdir(path):
#                 os.remove(os.path.join(path, f))
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)


class FilterView(generic.ListView):
    model = Pelcon
    template_name = 'upload.html'
    context_object_name = 'files'
    paginate_by = 4

    def get_queryset(self):
        return Pelcon.objects.filter(owner=self.request.user.id)


class UpLoadMultiFile(LoginRequiredMixin, FormView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    form_class = UpLoad
    template_name = 'upload1.html'  # Replace with your template.
    success_url = '/download/'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        error_file = []

        if form.is_valid():
            # clear data
            Pelcon.objects.all().delete()
            FileFormUpLoad.objects.all().delete()
            # exc clean file
            for f in files:
                instance = FileFormUpLoad(file=f, owner=self.request.user.id)
                instance.save()
                subprocess.run(
                    'python2 /home/s/Desktop/exefilter/ExeFilter.py /home/s/Desktop/djangoProject1/document/' + str(
                        f.name) + ' ' + '-d' + ' ' + '/home/s/Desktop/djangoProject1/store/document' + "/" + str(
                        self.request.user.id), shell=True)
            # get form from user folder to save
            try:
                for i in os.listdir('/home/s/Desktop/djangoProject1/store/document' + '/' + str(self.request.user.id)):
                    instance = Pelcon(pdf='/store/document/' + str(self.request.user.id) + '/' + i,
                                      owner=self.request.user.id, name=i)
                    if instance:
                        instance.save()
                    else:
                        return HttpResponse('/error')
                path1 = "/home/s/Desktop/djangoProject1/document/"
                for file in os.listdir(path1):
                    print(os.path.exists(path1 + '/' + file))
                    if not os.path.exists('/home/s/Desktop/djangoProject1/store/document' + '/' + str(
                            self.request.user.id) + '/' + file):
                        error_file.append(file)
                if len(error_file) > 0:
                    for error in error_file:
                        messages.error(self.request, error, extra_tags="error_file")
            except Exception as e:
                return render(request, 'index.html', {'error': e})
            time.sleep(0.5)
            path = '/home/s/Desktop/djangoProject1/document'
            for f in os.listdir(path):
                os.remove(os.path.join(path, f))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def delete_item(request, name):
    event = Pelcon.objects.get(name=name)
    event.delete()
    path = '/home/s/Desktop/djangoProject1/document'
    for f in os.listdir(path):
        os.remove(os.path.join(path, f))
    return redirect('/download/')
