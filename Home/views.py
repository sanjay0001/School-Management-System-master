from django.shortcuts import render,redirect
from .models import Student, Teacher
import datetime, jwt
# Create your views here.

#home page renderer
def home(request):
    return render(request, "home.html")

#student_register page renderer
def student_register(request):
    #invokes when form is submitted
    if request.method=="POST":
        name = request.POST.get("name")
        regno = request.POST.get("regno")
        standard = int(request.POST.get("standard"))
        section = request.POST.get("section")
        stream = request.POST.get("stream")
        password = request.POST.get("password")
        #search the student object in the database
        temp = Student.objects.filter(regno=regno)
        if temp:
            #if student present then navigate to the student_register page
            return render(request, "student_register.html", {'show':1})
        Student.objects.create(name=name, regno=regno, standard=standard,section=section,stream=stream, password=password)
        return redirect("login")
    #invokes when the page is requested by get method
    return render(request, "student_register.html",{'show':0})

#same as student register page
def teacher_register(request):
    if request.method=="POST":
        name = request.POST.get("name")
        teacherid = request.POST.get("teacherid")
        contact = request.POST.get("contact")
        subject = request.POST.get("subject")
        classestaught = request.POST.get("classestaught")
        password = request.POST.get("password")
        temp = Teacher.objects.filter(teacherid=teacherid)
        if temp:
            return render(request, "teacher_register.html", {'show':1})
        Teacher.objects.create(name=name, teacherid=teacherid, contact=contact,subject=subject,
        classestaught=classestaught, password=password)
        return redirect("login")
    return render(request, "teacher_register.html", {'show':0})

#invokes when login page is requested
def login(request):
    #checks for the post method
    if request.method=="POST":
        id=request.POST.get("regno")
        password = request.POST.get("password")
        temp = Student.objects.filter(regno=id, password=password)
        
        if temp:
            #if student is present then create a token and store it in the cookie and redirect to the student_profile page 
            payload = {
                'id':id+"1",
                'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat':datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')

            response = redirect("student_profile")

            response.set_cookie(key='jwt', value=token, httponly=True)
            
            return response

        temp = Teacher.objects.filter(teacherid=id, password=password)
        #same like student profile
        if temp:
            payload = {
                'id':id+"2",
                'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat':datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')

            response = redirect("teacher_profile")

            response.set_cookie(key='jwt', value=token, httponly=True)
            
            return response
        else:
            return render(request,"login.html", {'show':1})

        
    return render(request,"login.html", {'show':0})

def student_profile(request):
    #get the token from the cookie
    token = request.COOKIES.get('jwt')
    #if token is not present then redirect to the login page
    if not token:
        return redirect("login")
    #if token is present then decode the token and get the id
    try:
        payload = jwt.decode(token, 'secret', 'HS256')
    except jwt.ExpiredSignatureError:
        return redirect("login")
    
    temp=payload['id']
    #if it is teacher then redirect to login page
    if temp[-1]=='2':
        return redirect("login")
    #fetches the student object from the database
    temp1 = Student.objects.filter(regno=temp[:-1])
    #renders the student_profile page
    return render(request, "student_profile.html",{'name':temp1[0].name,'regno':temp1[0].regno,'standard':temp1[0].standard,'section':temp1[0].section,'stream':temp1[0].stream})
#same as student profile
def teacher_profile(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return redirect("login")
    
    try:
        payload = jwt.decode(token, 'secret', 'HS256')
    except jwt.ExpiredSignatureError:
        return redirect("login")
    temp=payload['id']
    if temp[-1]=='1':
        return redirect("login")
    temp1 = Teacher.objects.filter(teacherid=temp[:-1])
    return render(request, "teacher_profile.html", {'name':temp1[0].name})