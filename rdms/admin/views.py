from django.shortcuts import render,redirect,get_object_or_404
from predict.models import user
from doctor.models import Leave_doctor
from patient.models import Appointment_s

# Create your views here.
def manage_patients(request):
    patients = user.objects.filter(role='0')
    return render(request, 'manage_patients.html', {'patients': patients})

def delete_patient(request, patient_id):
    patient = get_object_or_404(user, id=patient_id, role='0')
    patient.delete()
    return redirect('manage_patients')

def manage_doctors(request):
    doctors = user.objects.filter(role='1').exclude(id=10)
    return render(request, 'manage_doctors.html', {'doctors': doctors})


def delete_user(request, user_id):
    doctor = get_object_or_404(user, id=user_id, role='1')
    doctor.delete()
    return redirect('manage_doctors')  # Redirect back to the doctor list


def admin_dashboard(request):
    
    return render(request,'admin.html')


def manage_leave_requests(request):
    # Optional: Only allow admin or logged-in user
    if not request.session.get('user_id'):
        return redirect('login')

    # Get all leave applications
    leaves = Leave_doctor.objects.select_related('userid').order_by('-date')

    return render(request, 'manage-leaves.html', {'leaves': leaves})

def update_leave_status(request, leave_id, action):
    leave = get_object_or_404(Leave_doctor, id=leave_id)

    # Only allow update if it's still pending
    if leave.status == 0:
        if action == 'approve':
            leave.status = 1  # Approved
            leave.save()

            # Cancel all appointments for this doctor on the same date
            Appointment_s.objects.filter(
                doctorid=leave.userid,
                date=leave.date
            ).update(status=1)  # 1 = Cancelled due to leave

        elif action == 'reject':
            leave.status = 2  # Rejected
            leave.save()

    return redirect('manage_leave_requests')