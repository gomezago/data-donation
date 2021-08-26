from django.shortcuts import render
import json
from .forms import ProjectForm, DonateForm
from .models import Project, Donation
from utils.bucket_functions import *
from .clue_functions import read_clue_file, transform_clue_dict, send_clue_data

def bucket_hello(request):
    project = Project.objects.all()
    context = {
        'project': project
    }
    return render(request, 'bucket_hello.html', context)

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
            # Initialize Thing and Properties in Bucket
            thingId, initialized_property_dict = initialize_donation(project, request.session['token'])

            # Read Data File
            data = json.load(form.cleaned_data['data'])
            data_dict = read_clue_file(data['data'])
            bucket_data_dict = transform_clue_dict(data_dict)

            send_clue_data(thingId, bucket_data_dict, initialized_property_dict, request.session['token'])

            # Save Donation
            donation = Donation(
                    user        = request.user,
                    data = project.data, #TODO: Allow for choice
                    project     = project,
                    updates     = form.cleaned_data['updates'],
                    adult       = form.cleaned_data['adult'],
                    consent      = form.cleaned_data['consent'],
                    thingId     = thingId,
                    propertyId  = initialized_property_dict,
                )
            donation.save()
            return render(request, 'project_view.html', {'project': project, 'form': form})
        else:
            print("Something went wrong with the Form...") #TODO: Raise Message
    else:
        form = DonateForm()
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

def initialize_donation(project, token):
    thing = new_thing(project.title, project.description, project.description)
    thing = create_thing(thing, token)
    if thing.ok:
        print("Thing created")
        thingId = thing.json()['id']

        initialized_property_dict = {}
        for key, value in project.data.items():
            property = new_property(type=key, description=value[1], name=value[0])
            property = create_property(thingId, property, token)
            if property.ok:
                print("Property created")
                propertyId = property.json()['id']
                initialized_property_dict[key] = propertyId

                consent = new_consent([project.groupId], ['dcd:read'])
                consent = grant_consent(thingId, propertyId, consent, token)

    return thingId, initialized_property_dict
