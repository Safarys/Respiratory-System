from django.shortcuts import render,redirect
from predict.models import user
from django.contrib import messages


# Create your views here.
def login(request):
    print("hellohow")
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)

        us=user.objects.filter(email=email).first()
        if us and us.password==password:
            if us.role=="0":
                return redirect('patients_dash')

            
       # print(us)

    return render(request, 'login.html')

def register(request):

    if request.POST:
        username = request.POST.get('first_name')
        lastname=request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob=request.POST.get('dob')
        gender=request.POST.get('gender')
        address=request.POST.get('address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password==confirm_password:
            user.objects.create(
                firstname=username,
                lastname=lastname,
                email=email,
                phone=phone,
                dob=dob,
                gender=gender,
                address=address,
                password=password,
            )
        else:
            messages.error(request, "Passwords do not match")

    return render(request, "reg.html")

def home(request):
    return render(request, 'home.html')