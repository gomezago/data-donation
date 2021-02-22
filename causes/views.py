from django.shortcuts import render
from causes.models import Cause

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
    context = {
        'cause' : cause
    }
    return render(request, "cause_detail.html", context)