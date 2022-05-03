from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
import logging
from bucket_view.models import Donation, DeletedPoint, Awareness
from bucket_view.views import initialize_donation_points, delete_property_timestamps, create_scatter, send_metadata
from bucket_view.forms import MotivationForm, AwarenessSurveyForm, MetadataForm, DeleteSurveyForm
from .forms import DeleteMotivationForm
from django.template.loader import render_to_string, get_template
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from utils.bucket_functions import delete_thing

logger = logging.getLogger('data_donation_logs')

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


def explore_point(request, pk):

    donation = Donation.objects.get(pk=pk)
    donation_thing = donation.thingId
    donation_speech_property = donation.propertyId['SPEECH_RECORD']

    # Create Graph
    points = initialize_donation_points(donation_thing, donation_speech_property, request.session['token'])

    # Pass Points
    dash_context = request.session.get('django_plotly_dash', dict())
    dash_context['django_to_dash_context'] = points
    dash_context['token'] = request.session['token']
    dash_context['thing_id'] = donation_thing
    dash_context['property'] = donation_speech_property
    request.session['django_plotly_dash'] = dash_context

    meta_form = MetadataForm()

    if request.method == 'POST' and 'confirm' in request.POST:
        meta_form = MetadataForm(request.POST)
        if meta_form.is_valid():
            send_metadata(donation, request.session['token'], meta_form.cleaned_data['sex'], meta_form.cleaned_data['age'], meta_form.cleaned_data['lan'],
                          meta_form.cleaned_data['acc'], meta_form.cleaned_data['dev'], meta_form.cleaned_data['use'])
            awareness = Awareness(
                donation = donation,
                awareness = meta_form.cleaned_data['awa']
            )
            awareness.save()
            #messages.success(request, "Thank you for your Donation!")


            if donation.participate:
                context_message = {'email_project': donation.project.title, 'email_username': request.user.username}
                html_message = get_template('email_card_thanks.html').render(context_message)
                subject = 'VoxPop: Thank you for your donation'

                email_msg = EmailMessage(subject, html_message, 'noreply@datadonation.ide.tudelft.nl', [request.user.email,], bcc=['datadonation-ide@tudelft.nl', ])
                email_msg.content_subtype = 'html'
                email_msg.send()
                #send_email_task.apply_async((subject, html_message, 'noreply@datadonation.ide.tudelft.nl', [request.user.email, ], ['datadonation-ide@tudelft.nl', ]))

            if meta_form.cleaned_data['awa'] == True:
                dash_context = request.session.get('django_plotly_dash',dict())
                dash_context['django_to_dash_context'] = points
                dash_context['token'] = request.session['token']
                dash_context['thing_id'] = donation_thing
                dash_context['property'] = donation_speech_property
                request.session['django_plotly_dash'] = dash_context


                delete_form = DeleteMotivationForm()

                return render(request, 'point_selection.html', {'donation' : donation, 'form' : delete_form})
            else:
                form = AwarenessSurveyForm()
                scatter = create_scatter(points)
                return render(request, 'survey_view.html', {'donation': donation, 'form': form, 'plot':scatter})

        else:
            messages.error(request, "Oops... Something went wrong. Please try again!")
    elif request.method == 'POST' and 'delete' in request.POST:
        # Delete Thing and Properties.
        delete_request = delete_thing(donation.thingId, request.session['token'])
        if delete_request.ok:
            # Delete Donation from DB
            Donation.objects.get(pk=pk).delete()
            logger.info("User {} deleted donation to project {}".format(request.user.username, donation.project.title))
        else:
            logger.error("User {} failed to delete donation to project {}".format(request.user.username, donation.project.title))
        del_form = DeleteSurveyForm()

        return render(request, 'delete_survey_view.html', {'form' : del_form})

    return render(request, "point_exploration.html", {'donation': donation, 'form': meta_form, })







#KWARGS:
# callback_context : Dash Callback Context
# dash_app : DashApp model instance
# dash_app_id
# request : Django Request Object
# session_state: Dictionary of information that is unique to this user session. # Any changes made to its content are persisted as part of the session.
# user: Django User

