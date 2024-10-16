from sqlite3 import IntegrityError
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
import cv2
from face_recognition import face_encodings,compare_faces
from pickle import dumps,loads
from os import path,makedirs,remove
from base64 import b64decode
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib import messages

def handling_404(request,exception):
    return render(request,'404.html',{'title':'404 Page'})

def home(request):
    return render(request,'home.html',{'title':'Digital ID'})

def about(request):
    return render(request,'about.html',{'title':'About Us'})

def registerationSuccessfull(request):
    return render(request,'success.html',{'title':'Registeration Succefull'})

class College:
    def adminLogin(request):
        context={}
        context['title']='College Login'
        context['label']='College Admin'
        if request.method == 'POST':
            try:
                adminData = collegeAdmin.objects.get(username=request.POST['username'])
                if adminData.password == request.POST['password']:
                    context['collegeName'] = adminData.collegeName
                    return redirect('/dashboard/student/?collegeName={}&searchDept=all&searchName='.format(adminData.collegeName))
                else:
                    context['message']='Wrong Password'
            except:
                context['message']='Wrong Username'
        return render(request,'login.html',context)
    
    def studentDashboard(request):
        context={}
        context['title']='Student Dashboard'
        if request.method == 'GET':
            if request.GET['searchDept'] == 'all':
                context['data']=studentModel.objects.filter(
                    collegeName=request.GET['collegeName'],
                    studentName__icontains=request.GET['searchName'])
            else:
                context['dept']=request.GET['searchDept']
                context['data']=studentModel.objects.filter(
                    collegeName=request.GET['collegeName'],
                    dept=context['dept'],
                    studentName__icontains=request.GET['searchName'])
            context['collegeName']=request.GET['collegeName']
        return render(request,'dashboard.html',context)
    
    def staffDashboard(request):
        context={}
        context['title']='Staff Dashboard'
        if request.method == 'GET':
            if request.GET['searchDept'] == 'all':
                context['data']=staffModel.objects.filter(
                    collegeName=request.GET['collegeName'],
                    staffName__icontains=request.GET['searchName'])
            else:
                context['dept']=request.GET['searchDept']
                context['data']=staffModel.objects.filter(
                    collegeName=request.GET['collegeName'],
                    dept=context['dept'],
                    staffName__icontains=request.GET['searchName'])
            context['collegeName']=request.GET['collegeName']
        return render(request,'dashboard.html',context)
    
    def removeData(request,nameSlug):
        try:
            studentData = studentModel.objects.get(name_slug=nameSlug)
            collegeName = studentData.collegeName
            remove('media/'+str(studentData.img))
            studentData.delete()
            return redirect('/dashboard/student/?collegeName={}&searchDept=all&searchName='.format(collegeName))
        except:
            staffData = staffModel.objects.get(name_slug=nameSlug)
            collegeName = staffData.collegeName
            remove('media/'+str(staffData.img))
            staffData.delete()
            return redirect('/dashboard/staff/?collegeName={}&searchDept=all&searchName='.format(collegeName)) 
        
    def editData(request):
        context={}
        nameSlug=request.GET['nameSlug']
        studentData = studentModel.objects.filter(name_slug=nameSlug)
        if len(studentData)>0:
            context['data'] = studentData
            if request.method == 'POST':
                studentData[0].studentName = request.POST['name']
                studentData[0].email = request.POST['email']
                studentData[0].dept = request.POST['dept']
                studentData[0].year = request.POST['year']
                studentData[0].mobile = request.POST['mobile']
                studentData[0].addr = request.POST['addr']
                studentData[0].city = request.POST['city']
                studentData[0].save()
                return redirect('/dashboard/student/?collegeName={}&searchDept=all&searchName'.format(studentData[0].collegeName))
        else:
            staffData = staffModel.objects.filter(name_slug=nameSlug)
            context['data'] = staffData
            if request.method == 'POST':
                staffData[0].staffName = request.POST['name']
                staffData[0].email = request.POST['email']
                staffData[0].dept = request.POST['dept']
                staffData[0].desg = request.POST['desg']
                staffData[0].mobile = request.POST['mobile']
                staffData[0].addr = request.POST['addr']
                staffData[0].city = request.POST['city']
                staffData[0].save()
                return redirect('/dashboard/staff/?collegeName={}&searchDept=all&searchName'.format(staffData[0].collegeName))
        return render(request,'update.html',context)

class Student:
    def login(request):
        context={}
        context['title']='Student Login'
        context['label']='Student'
        if request.method == 'POST':
            try:
                studentData = studentModel.objects.get(username=request.POST['username'])
                if studentData.password == request.POST['password']:
                    return redirect('/student-login/profle/?slug={}'.format(studentData.name_slug))
                else:
                    context['message']='Wrong Password'
            except :
                context['message']='Wrong Username'
        return render(request,'login.html',context)
    
    def register(request):
        context={}
        if request.method == 'POST':
            context['firstName'] = request.POST['firstName']
            context['middleName'] = request.POST['middleName']
            context['lastName'] = request.POST['lastName']
            context['email'] = request.POST['email']
            context['collegeName'] = request.POST['collegeName']
            context['dept'] = request.POST['dept']
            context['year'] = request.POST['year']
            context['mobile'] = request.POST['mobile']
            context['addr'] = request.POST['addr']
            context['city'] = request.POST['city']
            context['img'] = request.FILES['img']
            try:
                studentModel.objects.create(
                studentName=request.POST['firstName']+' '+request.POST['middleName']+' '+request.POST['lastName'],
                username=request.POST['username'], password=request.POST['password'],
                email=request.POST['email'], collegeName=request.POST['collegeName'],
                dept=request.POST['dept'], year=request.POST['year'], mobile=request.POST['mobile'],
                addr=request.POST['addr'], city=request.POST['city'], img=request.FILES['img']
                ).save()
                studentData = studentModel.objects.get(username=request.POST['username'])
                img_data=cv2.imread('media/'+str(studentData.img))
                studentData.img_encoded = dumps(face_encodings(cv2.cvtColor(img_data,cv2.COLOR_BGR2RGB))[0])
                studentData.save()
                messages.success(request, 'Your Registeration has been done successfully.')
                return redirect('registeration-successfull/')
            except IndexError:
                studentData=studentModel.objects.get(username=request.POST['username'])
                remove('media/'+str(studentData.img))
                studentData.delete()
                context['imgMessage'] = 'Please upload a passport Size image for Digital ID in the form of image file'
            except cv2.error:
                studentData=studentModel.objects.get(username=request.POST['username'])
                remove('media/'+str(studentData.img))
                studentData.delete()
                context['imgMessage']='Please upload image file like jpg png only'
            except:
                context['message'] = 'Please choose different username'
        context['title'] = 'Student Registeration'
        context['colleges'] = collegeAdmin.objects.all()
        return render(request,'register.html',context)
    
    def profile(request):
        context={}
        context['title']='Student Profile'
        context['data']=studentModel.objects.filter(name_slug=request.GET['slug'])
        if len(context['data']) == 0:
            return redirect('/student-login/')
        return render(request,'profile.html',context)

class Staff:
    def login(request):
        context={}
        context['title']='Staff Login'
        context['label']='Staff'
        if request.method == 'POST':
            try:
                staffData = staffModel.objects.get(username=request.POST['username'])
                if staffData.password == request.POST['password']:
                    return redirect('/staff-login/profle/?slug={}'.format(staffData.name_slug))
                else:
                    context['message']='Wrong Password'
            except :
                context['message']='Wrong Username'
        return render(request,'login.html',context)
    
    def register(request,college_name):      
        context={}
        context['title'] = 'Staff Registeration'
        context['collegeName'] = college_name
        try:
            context['id'] = int(staffModel.objects.last().username)+1
        except:
            context['id'] = 11111
        if request.method == 'POST':
            context['firstName'] = request.POST['firstName']
            context['middleName'] = request.POST['middleName']
            context['lastName'] = request.POST['lastName']
            context['email'] = request.POST['email']
            context['dept'] = request.POST['dept']
            context['desg'] = request.POST['desg']
            context['mobile'] = request.POST['mobile']
            context['addr'] = request.POST['addr']
            context['city'] = request.POST['city']
            context['img'] = request.FILES['img']
            try:
                staffModel.objects.create(
                staffName=request.POST['firstName']+' '+request.POST['middleName']+' '+request.POST['lastName'],
                username=context['id'], password=request.POST['password'],
                email=context['email'], collegeName=college_name,
                dept=context['dept'], desg=context['desg'], mobile=context['mobile'],
                addr=context['addr'], city=context['city'], img=context['img']
                ).save()
                staffData = staffModel.objects.get(username=context['id'])
                img = staffData.img
                img_data = cv2.imread('media/'+str(img))
                rgb_img = cv2.cvtColor(img_data,cv2.COLOR_BGR2RGB)
                img_encoding = face_encodings(rgb_img)[0]
                serialized_img = dumps(img_encoding)
                staffData.img_encoded = serialized_img
                staffData.save()
                return redirect('/dashboard/staff/?collegeName={}&searchDept=all&searchName'.format(college_name))
            except:
                staffData=studentModel.objects.get(username=request.POST['username'])
                remove('media/'+str(staffData.img))
                staffData.delete()
                context['imgMessage'] = 'Please upload a passport Size image for Digital ID in the form of image file'
        return render(request,'register.html',context)
    
    def profile(request):
        context={}
        context['title']='Staff Profile'
        context['data']=staffModel.objects.filter(name_slug=request.GET['slug'])
        if len(context['data']) == 0:
            return redirect('/staff-login')
        return render(request,'profile.html',context)
    
    def facescan(request):
        context={}
        context['title'] = 'Face Recognition'
        college_name = request.GET['collegeName']
        staffId = request.GET['data']
        if request.method == 'POST':
            try:
                decoded_image_data = b64decode(request.POST['image_data'].split(',')[1])
                makedirs('media/scaned-faces/',exist_ok=True)
                image_filename = path.join('media/scaned-faces/',str(staffId)+'.jpg')
                with open(image_filename,'wb') as f:
                    f.write(decoded_image_data)
                img2=cv2.imread(image_filename)
                img_encoding2=face_encodings(cv2.cvtColor(img2,cv2.COLOR_BGR2RGB))[0]
                studentData = studentModel.objects.filter(collegeName=college_name)
                for i in studentData:
                    if compare_faces([loads(i.img_encoded)],img_encoding2)[0] == True:
                        return redirect('/staff-login/scan-face/profile/?slug={}'.format(i.name_slug)) 
                context['message'] = 'Face Not Found'
            except :
                context['message'] = 'Please Clear the Camera'
        return render(request,'faceRecon.html',context)
    
    