from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
import logging
from bucket_view.models import Donation, DeletedPoint, Awareness, Project, City
from bucket_view.views import initialize_donation_points, delete_property_timestamps, create_scatter, send_metadata
from bucket_view.forms import MotivationForm, AwarenessSurveyForm, MetadataForm, DeleteSurveyForm
from .forms import DeleteMotivationForm, SelectDonationForm
from django.template.loader import render_to_string, get_template
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from utils.bucket_functions import delete_thing, read_shared_property_data
from django.contrib.auth.decorators import login_required
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio


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
            donation_city = City(
                donation = donation,
                city = meta_form.cleaned_data['city'],
            )
            donation_city.save()

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

@login_required()
def receiver_view(request, pk):

    project = Project.objects.get(pk=pk)

    donations = Donation.objects.filter(project=project)
    if donations.exists():
        total_d = donations.count()
        participate = donations.filter(participate=True).count()
        updates = donations.filter(updates=True).count()

        donations_df = pd.DataFrame.from_records(donations.values())
        scatter = donations_scatter(donations_df)

        form = SelectDonationForm(choices=[(d.id, d.user) for d in donations])

        context = {'project': project, 'donations': donations,
                   'part': participate, 'upda': updates,
                   'no_part': int(total_d - participate),
                   'no_upda': int(total_d - updates), 'plot': scatter,
                   'form': form}
    else:
        context = {'project': project, 'donations': donations,
                   'part': 0, 'upda': 0,
                   'no_part': 0,
                   'no_upda': 0, 'plot': 'Not Available',
                   'form': SelectDonationForm(choices=[(0, "---")])}

    if request.method == 'POST':
        form = SelectDonationForm(request.POST, choices =[(d.id, d.user) for d in donations] )
        if form.is_valid():
            donation_id = form.cleaned_data['donation']
            donation = Donation.objects.get(pk=donation_id)
            donation_thing = donation.thingId
            donation_speech_property = donation.propertyId['SPEECH_RECORD']
            donation_project = donation.project.__str__()
            groupId = 'dcd:groups:' + donation_project

            # Create Graph
            points = initialize_shared_points(donation_thing, donation_speech_property, groupId,
                                              request.session['token'])

            # Pass Points
            dash_context = request.session.get('django_plotly_dash', dict())
            dash_context['django_to_dash_context'] = points
            dash_context['token'] = request.session['token']
            dash_context['thing_id'] = donation_thing
            dash_context['group_id'] = groupId
            dash_context['property'] = donation_speech_property
            request.session['django_plotly_dash'] = dash_context

            return render(request, 'receiver_exploration.html', {'donation': donation})
    return render(request, "receiver_view.html", context=context)

@login_required()
def receiver_explore(request, pk):

    donation = Donation.objects.get(pk=pk)
    donation_thing = donation.thingId
    donation_speech_property = donation.propertyId['SPEECH_RECORD']
    donation_project = donation.project.__str__()
    groupId = 'dcd:groups:'+donation_project

    # Create Graph
    points = initialize_shared_points(donation_thing, donation_speech_property, groupId, request.session['token'])

    # Pass Points
    dash_context = request.session.get('django_plotly_dash', dict())
    dash_context['django_to_dash_context'] = points
    dash_context['token'] = request.session['token']
    dash_context['thing_id'] = donation_thing
    dash_context['group_id'] = groupId
    dash_context['property'] = donation_speech_property
    request.session['django_plotly_dash'] = dash_context

    return render(request, 'receiver_exploration.html', context={'donation' : donation})

def initialize_shared_points(donation_thing, donation_speech_property, groupId, token):
    speech_data = read_shared_property_data(donation_thing, donation_speech_property, groupId, token)
    if speech_data.ok:
        point_list = speech_data.json()['values']
    else:
        point_list = []
    return point_list


def donations_scatter(donations):
    pio.templates.default = "plotly_white"
    # Create Graph
    donations['DateString'] = donations['timestamp'].dt.strftime("%m/%d/%Y, %H:%M")
    donations['Hour'] = donations['timestamp'].dt.hour

    # Plot
    def scatter():
        fig = px.scatter(donations, y=donations.index+1, x="timestamp", custom_data = ["user_id", "DateString"],
                      labels={
                          "y": "Donations",
                          "timestamp": "Date",
                      },
                      hover_name="timestamp",
                      hover_data={'timestamp': False, 'Hour': False, 'user_id': True, 'DateString': True, },
                      )
        fig.update_layout(clickmode='event+select')
        fig.update_yaxes(dtick=1)
        fig.update_traces(marker_size=10)
        fig.update_traces(hovertemplate='<b>Username:</b> %{customdata[0]} <br><b>Date:</b> %{customdata[1]}')
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div
    return scatter()



#KWARGS:
# callback_context : Dash Callback Context
# dash_app : DashApp model instance
# dash_app_id
# request : Django Request Object
# session_state: Dictionary of information that is unique to this user session. # Any changes made to its content are persisted as part of the session.
# user: Django User

