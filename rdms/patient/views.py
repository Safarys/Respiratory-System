from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from doctor.models import Doctor,Sheduler,Prescription
from predict.models import user
from django.db.models import Count, F
from .models import Appointments
from urllib.parse import urlencode
from django.conf import settings
from predict.models import DiagnosticTest
from patient.models import Appointment_s
from doctor.models import Leave_doctor
from datetime import datetime


# Create your views here.

def book_appointment(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')  # Redirect if not authenticated

    # Get all doctors (role=1)
    doctors = user.objects.filter(role='1')

    if request.method == 'POST':
        doctor_id = request.POST.get('doctorid')
        appointment_date = request.POST.get('date')

        try:
            appointment_date_obj = datetime.strptime(appointment_date, "%Y-%m-%d").date()
            patient = user.objects.get(id=user_id)
            doctor = user.objects.get(id=doctor_id)

            # Check if doctor is on approved leave for selected date
            is_on_leave = Leave_doctor.objects.filter(
                userid=doctor,
                date=appointment_date_obj,
                status=1  # Approved leave
            ).exists()

            if is_on_leave:
                return render(request, 'appointment_c.html', {
                    'doctors': doctors,
                    'error': 'Doctor is on leave for the selected date. Please choose another date or doctor.'
                })

            # Save appointment
            Appointment_s.objects.create(userid=patient, doctorid=doctor, date=appointment_date_obj, status=0)

            return render(request, 'appointment_c.html', {
                'doctors': doctors,
                'message': 'Appointment booked successfully.'
            })

        except user.DoesNotExist:
            return render(request, 'appointment_c.html', {
                'doctors': doctors,
                'error': 'Invalid doctor selected.'
            })

    return render(request, 'appointment_c.html', {'doctors': doctors})



def patient_appointments_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Ensure user is logged in

    # Get appointments for the logged-in patient
    appointments = Appointment_s.objects.filter(userid_id=user_id).select_related('doctorid').order_by('-date')

    return render(request, 'patient_appointments.html', {'appointments': appointments})










def patient_dashboard(request):
    
    return render(request,'patient.html')




def patientappointment(request):
    try:
        # Perform join using ORM
        appointments = (
            Sheduler.objects
            .select_related('userid', 'userid__doctor')  # Ensure joined model
            .filter(userid__doctor__isnull=False)  # Ensure doctor exists
            .annotate(
                schedule_id=F('id'),  # Get Sheduler ID
                booked_tokens=Count('appointments__id'),  # Count booked tokens
                available_tokens=F('no_tokens') - F('booked_tokens')  # Calculate available tokens
            )
            .values(
                'schedule_id',
                'userid__firstname',
                'userid__lastname',
                'userid__email',
                'userid__phone',
                'date_she',
                'time_from',
                'time_to',
                'no_tokens',
                'available_tokens',
                'userid__doctor__Specialization',
                'userid__doctor__medical_li_no',
                'userid__doctor__qualification',
            )
        )
        return render(request, 'appointment-booking-static.html', {'appointments': appointments})
    except Exception as e:
        return render(request, 'appointment-booking-static.html', {'error': str(e)})



    



def patientappointment_Sleep(request):
    try:
        appointments = (
            Sheduler.objects
            .select_related('userid', 'userid__doctor')
            .filter(userid__doctor__Specialization="Sleep")
            .annotate(
                schedule_id=F('id'),
                booked_tokens=Count('appointments__id'),  # Ensure correct reverse relation
                available_tokens=F('no_tokens') - F('booked_tokens')
            )
            .values(
                'schedule_id',
                'userid__firstname',
                'userid__lastname',
                'userid__email',
                'userid__phone',
                'date_she',
                'time_from',
                'time_to',
                'no_tokens',
                'available_tokens',
                'userid__doctor__Specialization',
                'userid__doctor__medical_li_no',
                'userid__doctor__qualification',
            )
        )
        return render(request, 'appointment-booking-static.html', {'appointments': appointments})
    except Exception as e:
        return render(request, 'appointment-booking-static.html', {'error': str(e)})

def patientappointment_Allergist(request):
    try:
        appointments = (
            Sheduler.objects
            .select_related('userid', 'userid__doctor')
            .filter(userid__doctor__Specialization="Allergist")
            .annotate(
                schedule_id=F('id'),
                booked_tokens=Count('appointments__id'),  # Ensure correct reverse relation
                available_tokens=F('no_tokens') - F('booked_tokens')
            )
            .values(
                'schedule_id',
                'userid__firstname',
                'userid__lastname',
                'userid__email',
                'userid__phone',
                'date_she',
                'time_from',
                'time_to',
                'no_tokens',
                'available_tokens',
                'userid__doctor__Specialization',
                'userid__doctor__medical_li_no',
                'userid__doctor__qualification',
            )
        )
        return render(request, 'appointment-booking-static.html', {'appointments': appointments})
    except Exception as e:
        return render(request, 'appointment-booking-static.html', {'error': str(e)})
    

def patientappointment_Pulmonologist(request):
    try:
        appointments = (
            Sheduler.objects
            .select_related('userid', 'userid__doctor')
            .filter(userid__doctor__Specialization="Pulmonologist")
            .annotate(
                schedule_id=F('id'),
                booked_tokens=Count('appointments__id'),  # Ensure correct reverse relation
                available_tokens=F('no_tokens') - F('booked_tokens')
            )
            .values(
                'schedule_id',
                'userid__firstname',
                'userid__lastname',
                'userid__email',
                'userid__phone',
                'date_she',
                'time_from',
                'time_to',
                'no_tokens',
                'available_tokens',
                'userid__doctor__Specialization',
                'userid__doctor__medical_li_no',
                'userid__doctor__qualification',
            )
        )
        return render(request, 'appointment-booking-static.html', {'appointments': appointments})
    except Exception as e:
        return render(request, 'appointment-booking-static.html', {'error': str(e)})





    

def book_shedule(request, id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        
        if not user_id:
            return redirect('login')  # Redirect to login if not authenticated
        
        # Ensure both the user and schedule exist
        user_instance = get_object_or_404(user, id=user_id)
        sheduler_instance = get_object_or_404(Sheduler, id=id)
        
        # Check for duplicate booking
        if Appointments.objects.filter(shedule_id=sheduler_instance, userid=user_instance).exists():
            return redirect('patientappointment')  # Redirect if booking already exists

        # Create the booking using object instances
        Appointments.objects.create(shedule_id=sheduler_instance, userid=user_instance)

        # Redirect to patientappointment with success
        return redirect('patientappointment')
    
    # Handle GET requests gracefully
    return redirect('patientappointment')


def prescription_new_page(request, id):
    # Get appointment details
    appointment = get_object_or_404(Appointments, id=id)
    doctor = get_object_or_404(user, id=appointment.shedule_id.userid.id)
    prescriptions = Prescription.objects.filter(userid=appointment.userid, shedule_id=appointment.shedule_id)
    
    context = {
        'prescriptions': prescriptions,
        'appointment': appointment,
        'doctor': doctor,
        'patient': appointment.userid,
    }
    
    return render(request, 'view-prescription.html', context)



def bookingshowpage(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'error.html', {'message': 'User not logged in'})
    
    # Fetch the bookings for the logged-in user
    bookings = Appointments.objects.filter(userid=user_id).select_related('shedule_id__userid')

    booking_data = []
    for booking in bookings:
        doctor_name = f"Dr. {booking.shedule_id.userid.firstname} {booking.shedule_id.userid.lastname}"
        booking_date = booking.shedule_id.date_she.strftime('%B %d, %Y')
        booking_data.append({
            'booking_id': f"BK-{booking.id}",
            'doctor_name': doctor_name,
            'booking_date': booking_date,
            'status': 'completed',  # Assuming completed status for now
            'prescription_id': f"RX{booking.id}",  # Example prescription ID
            'b_id':booking.id
        })

    return render(request, 'prescription-list-view.html', {'booking_data': booking_data})







def test_view(request):
    """Fetch and display reports for the logged-in user."""
    
    user_id = request.session.get('user_id')  # Ensure user_id is stored in session

    if not user_id:
        return render(request, 'report-table-interface.html', {'error': 'User not logged in'})

    # Fetch reports related to the patient/user
    reports = DiagnosticTest.objects.filter(patid=user_id).order_by('-created_at')

    # Format reports with Report ID and downloadable link
    formatted_reports = []
    for index, report in enumerate(reports, start=1):
        formatted_reports.append({
            'report_id': f"REP-{report.created_at.strftime('%Y-%m-%d')}-{index:03d}",
            'date': report.created_at.strftime('%d %B, %Y'),
            'report_url': f"{settings.MEDIA_URL}reports/{report.result}",
        })

    return render(request, 'report-table-interface.html', {'reports': formatted_reports})



