from django.shortcuts import render
import json
from .forms import ProjectForm, DonateForm, DemographicsForm
from django.contrib.auth.decorators import login_required
from .models import Project, Donation
from utils.bucket_functions import *
from .clue_functions import read_clue_file, transform_clue_dict, send_clue_data
from django.http import HttpResponseRedirect, JsonResponse



@login_required()
def bucket_hello(request):
    if request.method == 'POST':
        form = DemographicsForm(request.POST, request.FILES)
        if form.is_valid():
            timestamp = round(time.time()*1000)
            sex = form.cleaned_data['sex']
            date = form.cleaned_data['date_of_birth']
            sex_data = {'values': [[timestamp, int(sex[0])]]}
            print(sex_data)
            date_data = {'values':[[timestamp, date.day, date.month, date.year]]}
            print(date_data)
            # Initialize Thing and Properties in Bucket
            thingId, initialized_property_dict = initialize_demographics_donation(request.session['token'], sex_data, date_data)
            # Save Donation
            donation = Donation(
                user=request.user,
                data={'SEX': ['Sex', 'Sex'], 'DATE': ['Date', 'Date']},
                project=Project.objects.get(id = 'ddd_demo'),
                updates=False,
                adult=True,
                consent=True,
                thingId=thingId,
                propertyId=initialized_property_dict)
            donation.save()

            donations = Donation.objects.filter(user=request.user)
            return render(request, 'bucket_hello.html', {'donations': donations})
        else:
            print("Something went wrong with the Form...") #TODO: Raise Message
    else:
        form = DemographicsForm()
        donations = Donation.objects.filter(user=request.user)
        if not donations:
            return render(request, 'first_hello.html', {'form': form})
        else:
            return render(request, 'bucket_hello.html', {'donations': donations})

@login_required()
def donation_view(request, pk):
    donation = Donation.objects.get(pk=pk)
    if request.method == 'POST':
        # Delete Thing and Properties.
        delete_request = delete_thing(donation.thingId, request.session['token'])
        # Delete Donation from DB
        Donation.objects.get(pk=pk).delete()
        print(delete_request)
        project = Project.objects.all()
        #TODO: Try again if error
        return render(request, 'bucket_hello.html', {'project':project}) #TODO: Show your data has been deleted message
    return render(request, 'donation_view.html', {'donation': donation})

@login_required()
def bucket_new(request):
    if request.method == 'POST':
        property_types = get_property_types(request.session['token'])
        form = ProjectForm(request.POST, request.FILES, choices = property_types)
        if form.is_valid():
            print('Form is Valid')
            project_id = "ddd_" + form.cleaned_data['id'].lower()
            group = new_group(project_id,[request.user.user_id])
            group = create_group(group, request.session['token'])
            if group.ok:
                print(get_property_description(request.session['token'],form.cleaned_data['data']))
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
                        groupId='dcd:groups:'+project_id,
                        instructions=form.cleaned_data['instructions'],
                        researcher_name=form.cleaned_data['researcher_name'],
                        researcher_affiliation=form.cleaned_data['researcher_affiliation'],
                    )
                project.save()

                form = ProjectForm(choices=property_types)
                return render(request, 'bucket_new.html', {'form': form})
            else:
                print("Something went wrong with the Group...") #TODO: Deal with this
        else:
            print("Something went wrong with the Form...")  # TODO: Display message
    else:
        property_types = get_property_types(request.session['token'])
        form = ProjectForm(choices=property_types)
    return render(request, 'bucket_new.html',  {'form' : form})

def project_list(request):
    project = Project.objects.all().order_by('-start')
    context = {
        'project': project
    }
    return render(request, "project_list.html", context)


def project_view(request, pk):
    project = Project.objects.get(pk=pk)
    data_tuple = [(key, value[0]) for key, value in project.data.items()]

    if request.method == 'POST':
        form = DonateForm(request.POST, request.FILES, choices=data_tuple)
        if form.is_valid():
            # Initialize Thing and Properties in Bucket
            thingId, initialized_property_dict = initialize_donation(project, request.session['token'])

            #Read Data Choices
            choices = form.cleaned_data['data_selection']

            # Read Data File
            data = json.load(form.cleaned_data['data'])
            data_dict = read_clue_file(data['data'], choices)
            bucket_data_dict = transform_clue_dict(data_dict)
            print(data_dict)
            print(bucket_data_dict)

            send_clue_data(thingId, bucket_data_dict, initialized_property_dict, request.session['token'])

            # Save Donation
            donation = Donation(
                    user        = request.user,
                    data = project.data,
                    project     = project,
                    updates     = form.cleaned_data['updates'],
                    participate       = form.cleaned_data['participate'],
                    consent      = form.cleaned_data['consent'],
                    thingId     = thingId,
                    propertyId  = initialized_property_dict,
                )
            donation.save()

            return render(request, "donation_view.html", {'donation': donation})
        else:
            print("Something went wrong with the Form...") #TODO: Raise Message
    else:
        form = DonateForm(choices=data_tuple)
    return render(request, 'project_view.html', {'project': project, 'form': form})


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

        if sex_property.ok:
            sex_propertyId = sex_property.json()['id']
            update_sex = update_property(thingId, sex_propertyId, sex, token)
        if age_property.ok:
            age_propertyId = age_property.json()['id']
            update_age = update_property(thingId, age_propertyId, age, token)

    return thingId, {'SEX' : sex_propertyId, 'DATE': age_propertyId}

def initialize_donation(project, token):
    thing = new_thing(project.title, project.description, project.description)
    thing = create_thing(thing, token)
    if thing.ok:
        thingId = thing.json()['id']

        initialized_property_dict = {}
        for key, value in project.data.items():
            property = new_property(type=key, description=value[1], name=value[0])
            property = create_property(thingId, property, token)
            if property.ok:
                propertyId = property.json()['id']
                initialized_property_dict[key] = propertyId

                consent = new_consent([project.groupId], ['dcd:read'])
                consent = grant_consent(thingId, propertyId, consent, token)
                print(consent)
                #TODO: Store failed data, try again afterwards
                #TODO: LOG
    return thingId, initialized_property_dict

@login_required()
def get_data_count(request): #For User Dashboard

    data_array = []

    donations = Donation.objects.filter(user = request.user)
    print(donations) #Queryset

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
        response = read_property_data(donation_thing, v, request.session['token'])
        for value in response.json()['values']:
            values = len(value[1:])
            data_array.append({
                'name' : response.json()['name'],
                'timestamp' : value[0],
                'values' : values
                })

    return JsonResponse(data_array, safe=False)