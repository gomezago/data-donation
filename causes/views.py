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
                data=form.cleaned_data["data"],
                email=form.cleaned_data["email"],
                available=form.cleaned_data["available"],
                updates=form.cleaned_data["updates"],
                authorize=form.cleaned_data["permission"],
                cause= cause
            )
            donation.save()
            #return HttpResponseRedirect()
            messages.success(request, "Thank You! Your Donation was Received")
            context = {'cause' : cause, 'form': form}
            return render(request, "cause_thanks.html", context)
        else:
            # Redirect to same page if data is invalid
            context = {'cause': cause, 'form': form}
            return render(request, "cause_detail.html", context)
    else:
        form = DonationForm() # Empty form
        context = {'cause': cause, 'form': form}
        return render(request, "cause_detail.html", context)

def cause_thanks(request, pk):
    cause = Cause.objects.get(pk=pk)
    context = {'cause' : cause}
    render(request, "cause_thanks.html", context)


