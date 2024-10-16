"""
URL configuration for digitalID project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from faceRecon import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.home,name='home'),
    path('college-login/',views.College.adminLogin,name='collegeLogin'),
    path('dashboard/student/',views.College.studentDashboard,name='dashboard'),
    path('dashboard/staff/',views.College.staffDashboard,name='dashboard-staff'),
    path('dashboard/staff-register/<college_name>',views.Staff.register,name='staffRegister'),
    path('dashboard/staff/update/',views.College.editData),
    path('staff-login/',views.Staff.login,name='staffLogin'),
    path('staff-login/profle/',views.Staff.profile,name='staffProfile'),
    path('student-login/',views.Student.login,name='studentLogin'),
    path('student-register/',views.Student.register,name='studentRegister'),
    path('student-login/profle/',views.Student.profile,name='studentProfile'),
    path('delete/<nameSlug>',views.College.removeData),
    path('dashboard/student/update/',views.College.editData),
    path('staff-login/scan-face/',views.Staff.facescan),
    path('staff-login/scan-face/profile/',views.Student.profile),
    path('about-us/',views.about),
    path('student-register/registeration-successfull/',views.registerationSuccessfull),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = 'faceRecon.views.handling_404'