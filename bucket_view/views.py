from django.shortcuts import render
import requests
from .forms import ProjectForm, DonateForm
from .models import Project, Donation

THING_URL = "https://dwd.tudelft.nl/bucket/api/things"

def bucket_hello(request):
    project = Project.objects.all()
    context = {
        'project': project
    }
    return render(request, 'bucket_hello.html', context)

def bucket_new(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = Project(
                user                = request.user,
                title               = form.cleaned_data['title'],
                description_tweet   = form.cleaned_data['description_tweet'],
                description         = form.cleaned_data['description_long'],
                hrec                = form.cleaned_data['hrec'],
                data                = form.cleaned_data['data'],
                image               = form.cleaned_data['image'],
                start               = form.cleaned_data['start'],
                end                 = form.cleaned_data['end'],
                data_info           = form.cleaned_data['data_info'],
            )
            project.save()

            thing = new_thing(project.title, project.description_tweet, project.data)
            create = create_thing(thing, request.session['token'])
            print(create) #TODO: Check for errors...

            form = ProjectForm()
            return render(request, 'bucket_new.html', {'form' : form})
        else:
            print("Something went wrong...") #TODO: Display message
    else:
        form = ProjectForm()
    return render(request, 'bucket_new.html',  {'form' : form})

def project_list(request):
    project = Project.objects.all()
    context = {
        'project': project
    }
    return render(request, "project_list.html", context)

def project_view(request, pk):
    project = Project.objects.get(pk=pk)

    if request.method == 'POST':
        form = DonateForm(request.POST, request.FILES)
        if form.is_valid():
            donation = Donation(
                user                = request.user,
                project             = project,
                updates             = form.cleaned_data['updates'],
            )
            donation.save()

            #thing = new_thing(project.title, project.description_tweet, project.data)
            #dd_thing = create_thing(thing, request.session['token'])
            #thingId = dd_thing.json()['id']

            #property = new_property(project.title, project.description, project.data)
            #dd_property = create_property(thingId, property, request.session['token'])
            #propertyId = dd_property.json()['id']

            #consent = new_consent([project.user.user_id, thingId], 'dcd:read')
            #dd_consent = grant_consent(thingId, propertyId, consent, request.session['token'])

            form = DonateForm()

            return render(request, 'project_view.html', {'project': project, 'form': form})
        else:
            print("Something went wrong...") #TODO: Fix this

    else:
        form = DonateForm()
    return render(request, 'project_view.html', {'project': project, 'form': form})

def new_thing(name, description, data):
    thing = {
        'name' : name,
        'description' : description,
        'type' : data,
        'pem' : None,
    }
    return thing

def new_property(name, description, type):
    property = {
        'name' : name,
        'description' : description,
        'type' : type,
        'typeId' : None,
    }
    return property

def new_consent(subjects, actions):
    consent = {
        'name' : subjects,
        'action' : actions,
    }
    return consent

def create_thing(thing, token):
    hed = {'Authorization': 'bearer ' + token['access_token']}
    response = requests.post(THING_URL, json=thing, headers=hed)

    if response.ok:
        thingId = response.json()['id']

    else:
        response.raise_for_status()
    return response

def create_property(thingId, property, token,):

    CREATE_PROPERTY_URL = f'https://dwd.tudelft.nl/bucket/api/things/{thingId}/properties'

    hed = {'Authorization': 'bearer ' + token['access_token']}
    par = {'thingId': thingId}
    response = requests.post(CREATE_PROPERTY_URL, json=property, headers=hed, params=par)

    if response.ok:
        propertyId = response.json()['id']
    else:
        response.raise_for_status()
        print(response.json())
    return response

def grant_consent(thingId, propertyId, consent, token):

    GRANT_CONSENT_URL = f'https://dwd.tudelft.nl/bucket/api/things/{thingId}/properties/{propertyId}/consents'

    hed = {'Authorization': 'bearer ' + token['access_token']}
    par = {'thingId': thingId, 'propertyId': propertyId}

    response = requests.post(GRANT_CONSENT_URL, json=consent, headers=hed, params=par)
    if response.ok:
        print(response.json())
    else:
        response.raise_for_status()
        print(response.json())
    return response