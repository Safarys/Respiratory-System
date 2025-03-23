from django.shortcuts import render, redirect,get_object_or_404
from .models import Sheduler
from patient.models import Appointments
from django.contrib import messages
from datetime import date
from .models import Prescription
from predict.models import user
from datetime import datetime



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

    # Print to check if it's fetching the patient ID correctly
    print("Appointments:", appointments)

    return render(request, 'doctor.html', {'appointments': appointments})

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
                        duration=duration
                    )
                saved_count += 1
                
            medicine_counter += 1
            
        if saved_count > 0:
            messages.success(request, f"{saved_count} medicines added to prescription successfully!")
            return redirect('doctordash')  # Redirect to the doctor dashboard or another appropriate page
        else:
            messages.error(request, "No valid medicine details provided.")
        
    return render(request, 'prescription.html', {'sheduler_id': id})