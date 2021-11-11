"""todowoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('signin/', views.signinuser, name='signinuser'),

    # Todos
    path('', views.homepage, name='homepage'),
    path('current/', views.currenttasks, name='currenttasks'),
    path('completed/', views.completedtasks, name='completedtasks'),
    path('create/', views.createtask, name='createtask'),
    path('task/<int:task_pk>', views.viewtask, name='viewtask'),
    path('task/<int:task_pk>/complete', views.completetask, name='completetask'),
    path('task/<int:task_pk>/delete', views.deletetask, name='deletetask'),
]
