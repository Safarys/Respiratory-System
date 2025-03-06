from django.shortcuts import render,redirect

# Create your views here.

def patient_dashboard(request):
    
    return render(request,'patient.html')