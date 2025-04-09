from django.shortcuts import render,redirect
from predict.models import user
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from doctor.models import Doctor,Patient


# Create your views here.
def login(request):
    # print("hellohow")
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)

        us=user.objects.filter(email=email).first()
        if check_password(password, us.password):  # Compare the hashed password with the entered password         
                request.session['user_id'] = us.id  # Store user ID in the session
                if us.id==10:
                    return redirect('admin_dashboard')     
                elif us.role == "0":
                    return redirect('patients_dash')     
                elif us.role=="1":   
                    return redirect('doctordash')     
       # print(us)
    return render(request, 'login.html')



def register(request):
    if request.method == "POST":
        username = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        address = request.POST.get('address')

        if password == confirm_password:
            # Create a new user
            new_user = user.objects.create(
                firstname=username,
                lastname=lastname,
                email=email,
                phone=phone,
                password=make_password(password),
                role=0
            )

            # Add patient details linked to the new user
            Patient.objects.create(
                userid=new_user,  # Link to the created user
                dob=dob,
                gender=gender,
                address=address
            )

            messages.success(request, "Registration successful!")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, "reg.html")

def home(request):
    return render(request, 'home.html')



def doctorregister(request):
    if request.method == 'POST':
        username = request.POST.get('firstName')
        lastname = request.POST.get('lastName')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        

        if password == confirm_password:
            hashed_password = make_password(password)
            user_obj =user.objects.create(
                firstname=username,
                lastname=lastname,
                email=email,
                phone=phone,
                password=hashed_password,
                role=1
            )

            Specialization = request.POST.get('Specialization')
            medical_li_no = request.POST.get('medical_li_no')
            qualification = request.POST.get('qualification')
            doctor = Doctor.objects.create(
                userid=user_obj.id,  # Associate the Doctor with the user
                Specialization=Specialization,
                medical_li_no=medical_li_no,
                qualification=qualification
            )
            messages.success(request, "User created successfully")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, 'doctor_reg.html')