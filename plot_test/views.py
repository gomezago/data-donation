from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
from bucket_view.models import Donation, DeletedPoint
from bucket_view.views import initialize_donation_points, delete_property_timestamps, create_scatter
from bucket_view.forms import MotivationForm, AwarenessSurveyForm
from .forms import DeleteMotivationForm
from django.contrib import messages

# Create your views here.
def select_point(request, pk):

    donation = Donation.objects.get(pk=pk)
    donation_thing = donation.thingId
    donation_speech_property = donation.propertyId['SPEECH_RECORD']

    delete_form = DeleteMotivationForm()

    # Create Graph
    points = initialize_donation_points(donation_thing, donation_speech_property, request.session['token'])

    # Pass Points
    dash_context = request.session.get('django_plotly_dash', dict())
    dash_context['django_to_dash_context'] = points
    dash_context['token'] = request.session['token']
    dash_context['thing_id'] = donation_thing
    dash_context['property'] = donation_speech_property
    request.session['django_plotly_dash'] = dash_context

    if request.method == 'POST' and 'confirm' in request.POST:
        selection = request.session.get('django_plotly_dash', dict())
        delete_form = DeleteMotivationForm(request.POST)

        if selection['selected_points']:
            selected_list = selection['selected_points']['points']
            selected_time = [dic['customdata'][0] for dic in selected_list]
            delete_property_timestamps(donation_thing, donation_speech_property, selected_time,request.session['token'])

            if delete_form.is_valid():
                # Save Deleted Points
                del_entry = DeletedPoint(
                    donation    = donation,
                    point       = selected_time,
                    why         = delete_form.cleaned_data['delete_motive']
                )
                del_entry.save()
            else:
                messages.error(request, "Oops... Something went wrong with the form! Please try again")
                return render(request, 'point_selection.html', {'donation': donation, 'form': delete_form})

        form = AwarenessSurveyForm()
        points = initialize_donation_points(donation_thing, donation_speech_property, request.session['token'])
        scatter = create_scatter(points)

        return render(request, "survey_view.html", {'donation':donation, 'form':form, 'plot':scatter})

    return render(request, 'point_selection.html', {'donation': donation, 'form' : delete_form})

#KWARGS:
# callback_context : Dash Callback Context
# dash_app : DashApp model instance
# dash_app_id
# request : Django Request Object
# session_state: Dictionary of information that is unique to this user session. # Any changes made to its content are persisted as part of the session.
# user: Django User

