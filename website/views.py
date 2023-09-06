from datetime import date
from django.shortcuts import render, redirect
from .forms import TokenRequestForm
from django.contrib import messages
from .download_appointment import render_to_pdf
from django.http import HttpResponse, response, FileResponse
from .utils import get_current_token, get_assign_token, increment_token, check_slot, add_patient, get_patients, clear_patients, reset_tokens, check_phone_number,slot_availability, get_slot_from_form
from django.contrib.auth.decorators import user_passes_test
from .pdf_format import generate_pdf


# Create your views here.
def index(request):
    return render(request, 'home.html')

def submit_token_form(request):
    choices = slot_availability()
    # Form1 >>>>>>>>>>>>
    if request.method =='POST':
        form = TokenRequestForm(choices,request.POST)
        if form.is_valid():
            selected_slot = choices[int(form.cleaned_data.get('book_for'))][1]
            p_name = form.cleaned_data.get('p_name')
            p_number = form.cleaned_data.get('p_number')
            if check_phone_number(p_number):
                return render(request, 'website/tokenform.html',{"same_number_alert":True})
            date,time = get_slot_from_form(selected_slot)
            my_token = str(get_assign_token(date,time))
            increment_token(date,time,"assign_token_")
            formatted_date = add_patient(p_name,p_number,my_token,date,time)
            generate_pdf(p_name, p_number, my_token, formatted_date , time)
            return FileResponse(open("my_appointment.pdf","rb"),content_type="application/pdf")
            #return render(request,'website/tokendisplay.html',{'name':name, 'phone_number':phone_number, 'reason_of_visit':reason_of_visit, 'my_token':my_token})
            
    else:
        # to - do redirect to another page if slots not available
        form = TokenRequestForm(choices)
        slot = check_slot()
        if slot == "morning":
            slot_time ="10:00am - 01:00pm "
            current_token = get_current_token(slot)
        elif slot == "evening":
            slot_time ="05:00pm - 08:00pm "
            current_token = get_current_token(slot)
        else:
            current_token =" - "
            slot_time =False
    return render(request, 'website/tokenform.html', {'form':form, 'current_token':current_token,"alert":False, "slot_time":slot_time})

@user_passes_test(lambda u:u.is_superuser)
def admin_page(request):
    if request.method=='POST':
        time = check_slot()
        if "update_current_token" in request.POST:
            increment_token("today",time,"current_token_")
        elif "reset_token" in request.POST:
            reset_tokens("today",time)
        elif "clear_patients" in request.POST:
            clear_patients()
        #to -do add reset visibility
    today_mdocuments,tomorrow_mdocuments = get_patients('morning')
    today_edocuments,tomorrow_edocuments = get_patients('evening')

    return render(request, 'website/admin_page.html',{'today_mdocuments':today_mdocuments,'today_edocuments':today_edocuments,"tomorrow_mdocuments":tomorrow_mdocuments,"tomorrow_edocuments":tomorrow_edocuments})



