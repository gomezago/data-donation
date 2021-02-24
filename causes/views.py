from django.shortcuts import render
from django.contrib import messages
from causes.models import Cause
from .forms import DonationForm
from causes.models import Donation
from django.http import HttpResponseRedirect
import datetime

# Create your views here.
def cause_index(request):
    causes = Cause.objects.all() # Query: Retrieving all objects in the projects table (all causes)
    # Context Dictionary, every view function needs a context dictionary
    context = {
        'causes' : causes # key: causes, to which we assign queryset containing all causes
    }
    return render(request, "cause_index.html", context) # Context is added to render so it will be available in template

def cause_detail(request, pk):
    cause = Cause.objects.get(pk=pk) # Query: Retrieves the project with primary key pk
    # If POST request we process the form
    if request.method == 'POST':
        # Create a form instance and populate it with data from request:
        form = DonationForm(request.POST, request.FILES)
        # Check if form is valid
        if form.is_valid():
            donation = Donation(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                data=form.cleaned_data["data"],
                available=form.cleaned_data["available"],
                cause= cause
            )
            donation.save()
            #return HttpResponseRedirect()
            messages.success(request, "Thank You! Your Donation was Received")
            context = {'cause' : cause, 'form': form}
    else:
        form = DonationForm()
        context = {'cause': cause, 'form': form}

    return render(request, "cause_detail.html", context)


