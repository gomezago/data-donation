import json
import logging
import pandas as pd
from django.shortcuts import render
from django.utils.html import format_html
from .forms import ProjectForm, DonateForm, DemographicsForm, MotivationForm, ReminderForm, MetadataForm, AwarenessSurveyForm, DeleteSurveyForm
from plot_test.forms import DeleteMotivationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Donation, Motivation, Awareness, InitialAwareness, FinalAwareness, DeleteDonation
from utils.bucket_functions import *
from .clue_functions import read_clue_file, transform_clue_dict, send_clue_data
from django.http import HttpResponseRedirect, JsonResponse
from operator import itemgetter
from django.core.mail import send_mail, EmailMessage
from bucket_view.tasks import send_email_task
from datetime import datetime, timedelta
from django.template.loader import render_to_string, get_template
from .google_functions import *
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio


logger = logging.getLogger('data_donation_logs')

@login_required()
def bucket_hello(request):
    project = Project.objects.all().order_by('-start')[:3]
    if request.method == 'POST':
        form = DemographicsForm(request.POST, request.FILES)
        if form.is_valid():
            timestamp = round(time.time()*1000)
            sex = form.cleaned_data['sex']
            if sex:
                sex_data = {'values': [[timestamp, int(sex[0])]]}
            else: sex_data = {}
            date = form.cleaned_data['date_of_birth']
            if date:
                date_data = {'values':[[timestamp, date.day, date.month, date.year]]}
            else: date_data = {}
            # Initialize Thing and Properties in Bucket
            thingId, initialized_property_dict = initialize_demographics_donation(request.session['token'], sex_data, date_data)
            # Save Donation
            donation = Donation(
                user=request.user,
                data={'SEX': ['Sex', 'Sex'], 'DATE': ['Date', 'Date']},
                project=Project.objects.get(id = 'ddd_demo'),
                updates=False,
                participate=True,
                consent=True,
                thingId=thingId,
                propertyId=initialized_property_dict)
            donation.save()
            logger.info("Donation by user {} to project {}".format(request.user.username, "Demographics"))
            donations = Donation.objects.filter(user=request.user)
            return render(request, 'bucket_hello.html', {'donations': donations, 'project':project})
        else:
            messages.error(request, "Oops... Something went wrong. Please try again!")
            return render(request, 'first_hello.html', {'form': form, 'project':project})
    else:
        form = DemographicsForm()
        donations = Donation.objects.filter(user=request.user)
        if not donations:
            return render(request, 'first_hello.html', {'form': form, 'project':project})
        else:
            return render(request, 'bucket_hello.html', {'donations': donations, 'project':project})

@login_required()
def donation_view(request, pk):
    donation = Donation.objects.get(pk=pk)

    if request.method == 'POST' and 'delete' in request.POST:
        # Delete Thing and Properties.
        delete_request = delete_thing(donation.thingId, request.session['token'])
        if delete_request.ok:
            # Delete Donation from DB
            Donation.objects.get(pk=pk).delete()
            logger.info("User {} deleted donation to project {}".format(request.user.username, donation.project.title))
        else:
            logger.error("User {} failed to delete donation to project {}".format(request.user.username, donation.project.title))

        project = Project.objects.all().order_by('-start')[:3]
        demo_form = DemographicsForm()
        donations = Donation.objects.filter(user=request.user)
        if not donations:
            messages.success(request, "Your data has been successfully deleted")
            return render(request, 'first_hello.html', {'form': demo_form, 'project': project})
        else:
            messages.success(request, "Your data has been successfully deleted")
            return render(request, 'bucket_hello.html', {'donations': donations, 'project':project})

    elif request.method == 'POST' and 'motivation' in request.POST:
        moti_form = MotivationForm(request.POST)
        if moti_form.is_valid():
            motivation = Motivation(
                user=request.user,
                project=donation.project,
                significance=moti_form.cleaned_data['significance'],
                curiosity = moti_form.cleaned_data['curiosity'],
                researcher = moti_form.cleaned_data['researcher'],
                participate = moti_form.cleaned_data['participate'],
                other = moti_form.cleaned_data['other'],
            )
            motivation.save()

            moti_form = MotivationForm()
            messages.success(request, "We have noted your answer! Thank you")
            return render(request, 'donation_view.html', {'donation': donation, 'form': moti_form})
        else:
            messages.error(request, "Oops... Something went wrong. Please try again!")
            return render(request, 'donation_view.html', {'donation': donation, 'form': moti_form})
    else:
        moti_form = MotivationForm()
    return render(request, 'donation_view.html', {'donation': donation, 'form': moti_form})



@login_required()
def metadata_view(request, pk):
    meta_form = MetadataForm()

    donation = Donation.objects.get(pk=pk)
    donation_thing = donation.thingId
    donation_speech_property = donation.propertyId['SPEECH_RECORD']

    # Create Graph
    points = initialize_donation_points(donation_thing, donation_speech_property, request.session['token'])
    scatter = create_scatter(points)

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

    context = {
        'donation' : donation,
        'plot': scatter,
        'form' : meta_form,
    }
    return render(request, 'metadata_view.html', context)


@login_required()
def survey_view(request, pk):
    form = AwarenessSurveyForm()

    donation = Donation.objects.get(pk=pk)
    donation_thing = donation.thingId
    donation_speech_property = donation.propertyId['SPEECH_RECORD']

    # Create Graph
    points = initialize_donation_points(donation_thing, donation_speech_property, request.session['token'])
    scatter = create_scatter(points)

    if request.method == 'POST':
        form = AwarenessSurveyForm(request.POST)
        if form.is_valid():
            awa = FinalAwareness(
                collected = form.cleaned_data['amount'],
                types = form.cleaned_data['types'],
                duration = form.cleaned_data['duration'],
                decision = form.cleaned_data['decision'],
                learn = form.cleaned_data['learn'],
            )
            awa.save()
            moti_form = MotivationForm()
            return render(request, 'donation_view.html', {'donation': donation, 'form': moti_form})
        else:
            messages.error(request, "Oops... Something went wrong. Please try again!")
            return render(request, 'survey_view.html', {'form': form, 'donation': donation, 'plot' : scatter})

    context = {
        'donation' : donation,
        'plot': scatter,
        'form' : form,
    }

    return render(request, 'survey_view.html', context=context)


@login_required()
def delete_survey_view(request):
    form = DeleteSurveyForm()

    if request.method == 'POST':
        form = DeleteSurveyForm(request.POST)
        if form.is_valid():
            deldo = DeleteDonation(
                user=request.user,
                collected = form.cleaned_data['amount'],
                types = form.cleaned_data['types'],
                duration = form.cleaned_data['duration'],
                decision = form.cleaned_data['decision'],
                learn = form.cleaned_data['learn'],
                delete = form.cleaned_data['delete'],
            )
            deldo.save()
            project = Project.objects.all().order_by('-start')[:3]
            demo_form = DemographicsForm()
            donations = Donation.objects.filter(user=request.user)
            if not donations:
                messages.success(request, "Thank you for contributing to our research!")
                return render(request, 'first_hello.html', {'form': demo_form, 'project': project})
            else:
                messages.success(request, "Thank you for contributing to our research!")
                return render(request, 'bucket_hello.html', {'donations': donations, 'project': project})
        else:
            messages.error(request, "Oops... Something went wrong. Please try again!")
            return render(request, 'delete_survey_view.html', {'form': form})

    context = {
        'form' : form,
    }

    return render(request, 'delete_survey_view.html', context=context)


@login_required()
def bucket_new(request):
    property_types = sorted(get_property_types(request.session['token']))
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, choices = property_types)
        if form.is_valid():
            project_id = "ddd_" + form.cleaned_data['id'].lower()
            group = new_group(project_id,[request.user.user_id])
            group = create_group(group, request.session['token'])
            if group.ok:
                #print(get_property_description(request.session['token'],form.cleaned_data['data']))
                project = Project(
                        user=request.user,
                        title=form.cleaned_data['title'],
                        id = project_id,
                        description_tweet=form.cleaned_data['description_tweet'],
                        description=form.cleaned_data['description_long'],
                        hrec=form.cleaned_data['hrec'],
                        data=get_property_description(request.session['token'],form.cleaned_data['data']),
                        image=form.cleaned_data['image'],
                        start=form.cleaned_data['start'],
                        end=form.cleaned_data['end'],
                        data_info=form.cleaned_data['data_info'],
                        data_ext=form.cleaned_data['data_ext'],
                        groupId='dcd:groups:'+project_id,
                        instructions=form.cleaned_data['instructions'],
                        researcher_name=form.cleaned_data['researcher_name'],
                        researcher_affiliation=form.cleaned_data['researcher_affiliation'],
                    )
                project.save()

                form = ProjectForm(choices=property_types)
                return render(request, 'bucket_new.html', {'form': form})
            else:
                logger.error("User {} failed to create new project {}".format(request.user.username))
                messages.error(request, "Oops... Something went wrong. Please try again!")
                return render(request, 'bucket_new.html', {'form': form})
        else:
            messages.error(request, "Oops... Something went wrong. Please try again!")
            return render(request, 'bucket_new.html', {'form': form})
    else:
        form = ProjectForm(choices=property_types)
    return render(request, 'bucket_new.html',  {'form' : form})

def project_list(request):
    project = Project.objects.all().order_by('-start')
    context = {
        'project': project,
    }
    return render(request, "project_list.html", context)


def project_view(request, pk):
    project = Project.objects.get(pk=pk)
    data_tuple = sorted([(key, value[0]) for key, value in project.data.items()])
    if pk == 'ddd_demo':
        if request.method == 'POST' and 'demo' in request.POST:
            form = DemographicsForm(request.POST, request.FILES)
            if form.is_valid():
                timestamp = round(time.time() * 1000)
                sex = form.cleaned_data['sex']
                if sex:
                    sex_data = {'values': [[timestamp, int(sex[0])]]}
                else:
                    sex_data = {}
                date = form.cleaned_data['date_of_birth']
                if date:
                    date_data = {'values': [[timestamp, date.day, date.month, date.year]]}
                else:
                    date_data = {}
                # Initialize Thing and Properties in Bucket
                thingId, initialized_property_dict = initialize_demographics_donation(request.session['token'],
                                                                                      sex_data, date_data)
                # Save Donation
                donation = Donation(
                    user=request.user,
                    data={'SEX': ['Sex', 'Sex'], 'DATE': ['Date', 'Date']},
                    project=Project.objects.get(id='ddd_demo'),
                    updates=False,
                    participate=True,
                    consent=True,
                    thingId=thingId,
                    propertyId=initialized_property_dict)
                donation.save()
                logger.info("Donation by user {} to project {}".format(request.user.username, "Demographics"))
                moti_form = MotivationForm()
                return render(request, "donation_view.html", {'donation': donation, 'form': moti_form})
            else:
                messages.error(request, "Oops... Something went wrong. Please try again!")
                return render(request, 'project_view.html', {'project': project, 'form': form,})
        else:
            form = DemographicsForm()
            return render(request, 'project_view.html', {'project': project, 'form': form,})
    else:

        if request.method == 'POST' and 'remind' in request.POST:
            reminder_form = ReminderForm(request.POST, request.FILES)
            if reminder_form.is_valid():
                email = reminder_form.cleaned_data['reminder_email']
                when = int(reminder_form.cleaned_data['reminder_time'])
                email_date = datetime.utcnow() + timedelta(weeks=when+1)

                context_message = {'email_project' : project.title, 'email_project_id' : project.pk}
                html_message = get_template('email_card.html').render(context_message)
                subject = 'VoxPop: Data Donation Reminder'

                #email_msg = EmailMessage(subject, html_message, 'noreply@datadonation.ide.tudelft.nl', [email,], bcc=['datadonation-ide@tudelft.nl', ])
                #email_msg.content_subtype = 'html'
                #email_msg.send()
                send_email_task.apply_async((subject, html_message, 'noreply@datadonation.ide.tudelft.nl', [email, ], ['datadonation-ide@tudelft.nl', ]), eta=email_date)
                messages.success(request, "Thank you for your interest! We will send you an email on " + email_date.strftime("%d-%m-%Y"))

                form = DonateForm(choices=data_tuple)
                return render(request, 'project_view.html',
                              {'project': project, 'form': form, 'reminder': reminder_form,})
            else:
                messages.error(request, "Oops... Please enter a valid email address!")
                form = DonateForm(choices=data_tuple)
                return render(request, 'project_view.html', {'project': project, 'form': form, 'reminder': reminder_form,})

        elif request.method == 'POST' and 'donate' in request.POST:
            form = DonateForm(request.POST, request.FILES, choices=data_tuple)
            if form.is_valid():

                if pk == 'ddd_period':
                    #Read Data Choices
                    choices = form.cleaned_data['data_selection']

                    # Initialize Thing and Properties in Bucket
                    thingId, initialized_property_dict = initialize_donation(project, choices, request.session['token'])

                    # Read Data File
                    data = json.load(form.cleaned_data['data'])
                    data_dict = read_clue_file(data['data'], choices)
                    bucket_data_dict = transform_clue_dict(data_dict)

                    send_clue_data(thingId, bucket_data_dict, initialized_property_dict, request.session['token'])

                    # Save Donation
                    donation = Donation(
                        user=request.user,
                        data=project.data,
                        project=project,
                        updates=form.cleaned_data['updates'],
                        participate=form.cleaned_data['participate'],
                        consent=form.cleaned_data['consent'],
                        thingId=thingId,
                        propertyId=initialized_property_dict,
                    )
                    donation.save()

                    logger.info("Donation by user {} to project {}".format(request.user.username, project.title))
                    moti_form = MotivationForm()
                    return render(request, "donation_view.html", {'donation': donation, 'form': moti_form})

                elif pk == 'ddd_voxpop':
                    # Read File
                    zip_file_dict = extract_zip(form.cleaned_data['data'])
                    # Validate File
                    valid = validate_voice(zip_file_dict.keys())
                    if valid:
                        #choices = form.cleaned_data['data_selection']
                        choices = {"SPEECH_RECORD": ["Speech Record", ""], "SPEAKER_METADATA": ["Speaker Metadata", "Speaker Metadata"]}

                        # Initialize Thing and Properties in Bucket
                        thingId, initialized_property_dict = initialize_bucket(project, choices, request.session['token'])

                        # Get Data
                        assistant_json = get_assistant_file(zip_file_dict)
                        metadata_list = get_metadata(assistant_json, zip_file_dict)

                        values, files = get_values_files(metadata_list)
                        req = update_property_media(thingId, initialized_property_dict['SPEECH_RECORD'], values, files, request.session['token'])
                        print(req.text)

                        # Save Donation
                        donation = Donation(
                                user        = request.user,
                                data = project.data,
                                project     = project,
                                updates     = form.cleaned_data['updates'],
                                participate       = form.cleaned_data['participate'],
                                consent      = True,
                                thingId     = thingId,
                                propertyId  = initialized_property_dict,
                            )
                        donation.save()

                        initial_awa = InitialAwareness(
                            donation    = donation,
                            collection  = form.cleaned_data['stored'],
                            takeout     = form.cleaned_data['takeout'],
                            goal        = form.cleaned_data['goal'],
                            info        = form.cleaned_data['info'],
                        )
                        initial_awa.save()

                        logger.info("Donation by user {} to project {}".format(request.user.username, project.title))

                        points = initialize_donation_points(thingId, initialized_property_dict['SPEECH_RECORD'], request.session['token'])
                        scatter = create_scatter(points)

                        meta_form = MetadataForm()
                        return render(request, "metadata_view.html", {'donation': donation, 'form' : meta_form, 'plot' : scatter})
                    else:
                        error_message = format_html("Oops... It seems that the file you uploaded is not what we expected!")
                        messages.error(request, error_message)
                        reminder_form = ReminderForm()
                        return render(request, 'project_view.html',
                                      {'project': project, 'form': form, 'reminder': reminder_form,})
            else:
                messages.error(request, "Oops... Something went wrong. Please try again!")
                reminder_form = ReminderForm()
                return render(request, 'project_view.html', {'project': project, 'form': form, 'reminder': reminder_form,})
        else:
            form = DonateForm(choices=data_tuple)
            reminder_form = ReminderForm()
            return render(request, 'project_view.html', {'project': project, 'form': form, 'reminder': reminder_form,})


def get_property_types(token):
    property_types = list_property_types(token)

    if property_types.ok:
        property_types = property_types.json()
        property_types_list = []
        for property in property_types:
            property_types_list.append((property['id'], property['name']), )

    return property_types_list

def get_property_description(token, selection):
    property_types = list_property_types(token)
    if property_types.ok:
        property_types = property_types.json()
        selected_properties = {}

        for property in property_types:
            for item in selection:
                if property['id'] == item:
                    selected_properties[property['id']] = property['name'], property['description']
                    break
    return selected_properties

def initialize_demographics_donation(token, sex, age):
    thing = new_thing('DDD Demographics', 'Demographic Data for DDD', 'We collect Demographic Data about the users of the DDD platform')
    thing = create_thing(thing, token)

    if thing.ok:
        thingId = thing.json()['id']
        sex_property = new_property(type='SEX', description='Sex', name='Sex')
        sex_property = create_property(thingId, sex_property, token)

        #Create Age Property:
        age_property = new_property(type='DATE', description='Date of Birth', name='Date of Birth')
        age_property = create_property(thingId, age_property, token)

        #Consent
        consent = new_consent(['dcd:groups:ddd_demo'], ['dcd:actions:read'])

        if sex_property.ok:
            sex_propertyId = sex_property.json()['id']
            if sex:
                update_property(thingId, sex_propertyId, sex, token)
                grant_consent(thingId, sex_propertyId, consent, token)
        if age_property.ok:
            age_propertyId = age_property.json()['id']
            if age:
                update_property(thingId, age_propertyId, age, token)
                grant_consent(thingId, age_propertyId, consent, token)
    else:
        logger.error("Initializing donation to project {}".format("Demographics"))

    return thingId, {'SEX' : sex_propertyId, 'DATE': age_propertyId}


def initialize_bucket(project, choices, token):
    selected_data_dict = {k: project.data[k] for k in choices}
    thing = new_thing(project.title, project.description_tweet, project.description_tweet)
    thing = create_thing(thing, token)
    if thing.ok:
        thingId = thing.json()['id']

        initialized_property_dict = {}
        for key, value in selected_data_dict.items(): #project.data.items():
            property = new_property(type=key, description=value[1], name=value[0])
            property = create_property(thingId, property, token)
            if property.ok:
                propertyId = property.json()['id']
                initialized_property_dict[key] = propertyId
                #consent = new_consent([project.groupId], ['dcd:actions:read'])
                #grant_consent(thingId, propertyId, consent, token)
            else:
                logger.error("Initializing properties in donation to project {}".format(project.title))
    else:
        logger.error("Initializing thing in donation to project {}".format(project.title))
    return thingId, initialized_property_dict


def initialize_donation(project, choices, token):
    selected_data_dict = {k: project.data[k] for k in choices}
    thing = new_thing(project.title, project.description_tweet, project.description_tweet)
    thing = create_thing(thing, token)
    if thing.ok:
        thingId = thing.json()['id']

        initialized_property_dict = {}
        for key, value in selected_data_dict.items(): #project.data.items():
            property = new_property(type=key, description=value[1], name=value[0])
            property = create_property(thingId, property, token)
            if property.ok:
                propertyId = property.json()['id']
                initialized_property_dict[key] = propertyId

                consent = new_consent([project.groupId], ['dcd:actions:read'])
                grant_consent(thingId, propertyId, consent, token)
            else:
                logger.error("Initializing properties in donation to project {}".format(project.title))
    else:
        logger.error("Initializing thing in donation to project {}".format(project.title))
    return thingId, initialized_property_dict

@login_required()
def get_data_count(request): #For User Dashboard

    data_array = []

    donations = Donation.objects.filter(user = request.user)

    for donation in donations:
        donation_thing = donation.thingId
        donation_properties = donation.propertyId

        for k, v in donation_properties.items():
            response = read_property_data(donation_thing, v, request.session['token'])

            data_array.append({
                    'name' : response.json()['name'],
                    'group' : donation.project.title,
                    'values' : len(response.json()['values']),
               })

    return JsonResponse(data_array, safe=False)

@login_required()
def get_data(request, pk): #For Single Donation

    donation = Donation.objects.get(pk = pk)
    donation_thing = donation.thingId
    donation_properties = donation.propertyId

    data_array = []
    for k, v in donation_properties.items():
        response = read_property_data_month(donation_thing, v, request.session['token'])
        for value in response.json()['values']:

            values = len(value[1:])
            data_array.append({
                'name' : response.json()['name'],
                'timestamp' : value[0],
                'values' : values
                })
    sorted_data_array = sorted(data_array, key=itemgetter('timestamp'))
    return JsonResponse(sorted_data_array, safe=False)

def initialize_donation_points(donation_thing, donation_speech_property, token):
    speech_data = read_property_data(donation_thing, donation_speech_property, token)
    if speech_data.ok:
        point_list = speech_data.json()['values']
    else:
        point_list = []
    return point_list

def create_scatter(point_list):
    pio.templates.default = "plotly_white"

    # Create Graph
    df = pd.DataFrame(point_list, columns=['Timestamp', 'Path', 'Transcript'])
    df['DateTime'] = pd.to_datetime(df['Timestamp'], unit='ms')
    df['DateString'] = df['DateTime'].dt.strftime("%m/%d/%Y, %H:%M")
    df['Hour'] = df['DateTime'].dt.hour
    # Plot
    def scatter():
        fig = px.scatter(df, x="DateTime", y="Hour", custom_data=["Timestamp", "DateString"], opacity=0.5,
                         labels={
                             "DateTime": "Date",
                             "Hour": "Hour",
                         },
                         hover_name="DateTime", hover_data={'DateTime': False, 'Hour': False, 'Transcript': True, 'DateString' : True, },
                         )

        fig.update_layout(clickmode='event+select')
        fig.update_traces(marker_size=10)
        fig.update_traces(hovertemplate='<b>Transcript:</b> %{customdata[2]} <br><b>Date:</b> %{customdata[1]}')
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div
    return scatter()


def send_metadata(donation, token, sex,age, language, accent, device, users):

    thingId = donation.thingId

    # Grant Consent
    consent = new_consent([donation.project.groupId], ['dcd:actions:read'])
    consent_records = grant_consent(thingId, donation.propertyId['SPEECH_RECORD'], consent, token)

    timestamp = round(time.time() * 1000)
    values= {'values': [[timestamp, int(sex), int(age), int(language), accent, int(device), int(users)]]}
    print(values)

    if not 'SPEAKER_METADATA' in donation.propertyId:
        # Create Property
        metadata_property = new_property(type='SPEAKER_METADATA', description='Speaker Metadata', name='Speaker Metadata')
        metadata_property = create_property(thingId, metadata_property, token)
        # Send Data
        if metadata_property.ok:
            propertyId = metadata_property.json()['id']
            update = update_property(donation.thingId, propertyId, values, token)
            print(update.text)
            grant_consent(thingId, propertyId, consent, token)

        # Update Property ID in Donation
        donation.propertyId['SPEAKER_METADATA'] = propertyId
        donation.save(update_fields=['propertyId'])
    else:
        propertyId = donation.propertyId['SPEAKER_METADATA']
        update = update_property(donation.thingId, propertyId, values, token)
        print(update.text)
        grant_consent(thingId, propertyId, consent, token)

