from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
from bucket_view.models import Donation
from bucket_view.views import initialize_donation_points, delete_property_timestamps
from bucket_view.forms import MotivationForm

# Create your views here.
def select_point(request, pk):

    donation = Donation.objects.get(pk=pk)
    donation_thing = donation.thingId
    donation_speech_property = donation.propertyId['SPEECH_RECORD']

    # Create Graph
    points = initialize_donation_points(donation_thing, donation_speech_property, request.session['token'])

    # Pass Points
    dash_context = request.session.get('django_plotly_dash', dict())
    dash_context['django_to_dash_context'] = points
    request.session['django_plotly_dash'] = dash_context

    if request.method == 'POST' and 'confirm' in request.POST:
        selection = request.session.get('django_plotly_dash', dict())
        if selection['selected_points']:
            selected_list = selection['selected_points']['points']
            selected_time = [dic['customdata'][0] for dic in selected_list]
            delete_selection = delete_property_timestamps(donation_thing, donation_speech_property, selected_time, request.session['token'])

        moti_form = MotivationForm()
        return render(request, "donation_view.html", {'donation': donation, 'form': moti_form})

    return render(request, 'point_selection.html', {'donation': donation})

#KWARGS:
# callback_context : Dash Callback Context
# dash_app : DashApp model instance
# dash_app_id
# request : Django Request Object
# session_state: Dictionary of information that is unique to this user session. # Any changes made to its content are persisted as part of the session.
# user: Django User

