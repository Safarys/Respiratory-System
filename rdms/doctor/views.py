from django.shortcuts import render, redirect,get_object_or_404
from .models import Sheduler
from patient.models import Appointments,Appointment_s
from django.contrib import messages
from datetime import date
from .models import Prescription,Patient,Leave_doctor
from predict.models import user
from datetime import datetime
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.utils.decorators import decorator_from_middleware
from django.middleware.cache import CacheMiddleware



def leave_status(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')  # ensure login check

    # Get leave records for the current doctor
    leaves = Leave_doctor.objects.filter(userid_id=user_id).order_by('-date')

    # Optional: Convert status codes to human-readable status
    for leave in leaves:
        if leave.status == 0:
            leave.status_text = "Pending"
        elif leave.status == 1:
            leave.status_text = "Approved"
        elif leave.status == 2:
            leave.status_text = "Rejected"
        else:
            leave.status_text = "Unknown"

    return render(request, 'leave-status.html', {'leaves': leaves})




def doctordash(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')  # Redirect if not authenticated

    current_date = date.today()

    # Fetch patient ID, names, and scheduler ID for today's appointments of the doctor
    appointments = (
        Appointments.objects
        .filter(shedule_id__userid=user_id, shedule_id__date_she=current_date)
        .select_related('userid', 'shedule_id')
        .values(
            'userid',  # This is the patient ID
            'userid__firstname',
            'userid__lastname',
            'shedule_id__id'  # Sheduler table ID
        )
    )
# 1. Appointments from Appointment_s (doctor’s direct appointments)
    doctor_appointments = (
        Appointment_s.objects
        .filter(doctorid_id=user_id, date=current_date)
        .select_related('userid')  # for patient info
        .values(
            'id',
            'userid__id',
            'userid__firstname',
            'userid__lastname',
            'date',
            'status'
        )
    )
    # Print to check if it's fetching the patient ID correctly
    print("Appointments:", appointments)
    print("Appointments:", doctor_appointments)


    return render(request, 'doctor.html', {'doctor_appointments':doctor_appointments,'appointments': appointments, 'user_id': user_id})


def shedulerdoctor(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')  # Redirect to login if user_id is not in session

        date = request.POST.get('date')
        time_from = request.POST.get('timeFrom')
        time_to = request.POST.get('timeTo')
        tokens = request.POST.get('tokens')

        # Validate inputs
        if not (date and time_from and time_to and tokens):
            messages.error(request, "All fields are required.")
            return render(request, 'schedule.html')

        try:
            # Convert tokens to integer
            tokens = int(tokens)
            
            # Convert date and time to valid formats
            date = datetime.strptime(date, "%Y-%m-%d").date()
            time_from = datetime.strptime(time_from, "%H:%M").time()
            time_to = datetime.strptime(time_to, "%H:%M").time()

            # Fetch the actual user object
            user_instance = user.objects.get(id=user_id)

            # Save data to database
            Sheduler.objects.create(
                userid=user_instance,  # Correct ForeignKey reference
                date_she=date,
                time_from=time_from,
                time_to=time_to,
                no_tokens=tokens
            )

            messages.success(request, "Schedule created successfully.")
            return redirect('shedulerdoctor')  # Redirect to avoid form resubmission

        except ValueError:
            messages.error(request, "Invalid input. Please check the entered values.")
        except user.DoesNotExist:
            messages.error(request, "User does not exist. Please log in again.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'schedule.html')


def view_shedules(request):
    user_id = request.session.get('user_id')  # Get user ID from session
    schedules = Sheduler.objects.filter(userid=user_id)  # Filter schedules by user ID

    return render(request, 'appointment-table.html', {'schedules': schedules})


def add_presicription(request, id,pid):
    user_id = pid
    doctor_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    if request.method == 'POST':
        # Get the user and schedule instances
        user_instance = get_object_or_404(user, id=user_id)
        sheduler_instance = get_object_or_404(Sheduler, id=id)

            # Loop through the form data to save multiple medicines
        medicine_counter = 1
        saved_count = 0
            
            # Continue checking as long as medicine fields exist
        while f'medicine-{medicine_counter}' in request.POST:
            medicine_name = request.POST.get(f'medicine-{medicine_counter}')
                
                # Only process if there's a medicine name
            if medicine_name:
                dosage = request.POST.get(f'dosage-{medicine_counter}', '')
                duration = request.POST.get(f'duration-{medicine_counter}', '')
                    
                    # Check if checkbox values are in the POST data
                morning = request.POST.get(f'morning-{medicine_counter}') is not None
                afternoon = request.POST.get(f'afternoon-{medicine_counter}') is not None
                evening = request.POST.get(f'evening-{medicine_counter}') is not None

                    # Insert into the database
                Prescription.objects.create(
                        shedule_id=sheduler_instance,
                        userid=user_instance,
                        medicine_name=medicine_name,
                        dosage=dosage,
                        morning=morning,
                        afternoon=afternoon,
                        evening=evening,
                        duration=duration,
                        doctor_id=doctor_id
                    )
                saved_count += 1
                
            medicine_counter += 1
            
        if saved_count > 0:
            messages.success(request, f"{saved_count} medicines added to prescription successfully!")
            return redirect('doctordash')  # Redirect to the doctor dashboard or another appropriate page
        else:
            messages.error(request, "No valid medicine details provided.")
        
    return render(request, 'prescription.html', {'sheduler_id': id})



def patient_view_page(request, id):
    # Fetch the patient object using `userid`
    patient = get_object_or_404(Patient, userid=id)

    # Get the associated user
    user = patient.userid  # Since `userid` is a ForeignKey to the User model

    # Combine user and patient details
    patient_details = {
        "first_name": user.firstname,
        "last_name": user.lastname,
        "email": user.email,
        "phone": user.phone,
        "dob": patient.dob,
        "gender": patient.gender,
        "address": patient.address,
    }

    return render(request, 'patient_view.html', {"patient": patient_details})






def prescription_doctor_view(request, userid):
    user_instance = get_object_or_404(user, id=userid)  # Get user instance correctly
    prescriptions = Prescription.objects.filter(userid=user_instance).order_by('-created_at')  # Use the instance

    return render(request, 'prescription_view.html', {
        'user': user_instance,
        'prescriptions': prescriptions
    })

def logout_view(request) -> HttpResponseRedirect:
    request.session.flush()  # Clear session
    return redirect('home')  # Redirect to login page


def doctor_appointments(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')  # Redirect if not authenticated

    try:
        doctor = user.objects.get(id=user_id, role='1')
    except user.DoesNotExist:
        return render(request, 'error.html', {'message': 'Unauthorized access'})

    # Retrieve all appointments for this doctor
    appointments = Appointment_s.objects.filter(doctorid=doctor)

    # Generate patient numbers (Self-incrementing)
    for idx, appointment in enumerate(appointments, start=1):
        appointment.patient_number = idx

    return render(request, 'doctor_appointments.html', {
    'appointments': appointments,
    'doctor_id': doctor.id,  # Ensure doctor_id is set properly
    'patient_ids': [appt.userid.id for appt in appointments]
})

def leave(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')  # Ensure user is logged in

    if request.method == 'POST':
        date_l = request.POST.get('date')
        reason = request.POST.get('reason')

        if date_l and reason:
            Leave_doctor.objects.create(userid_id=user_id, date=date_l, reason=reason,status=0)
            return render(request, 'leave-request-page.html', {'success': True})
        else:
            return render(request, 'leave-request-page.html', {'error': 'All fields are required.'})

    return render(request, 'leave-request-page.html')