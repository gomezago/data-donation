from django.shortcuts import render
import requests
from .forms import ProjectForm, DonateForm
from .models import Project, Donation
from utils.bucket_functions import new_group, new_consent, new_property, create_group, create_property, grant_consent, list_consent, list_property_types

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
            print(form.cleaned_data['data'])
            print(request.user.user_id)
            group = new_group(form.cleaned_data['title'].replace(" ", ""),[request.user.user_id])
            group = create_group(group, request.session['token'])
            if group.ok:
                project = Project(
                        user=request.user,
                        title=form.cleaned_data['title'],
                        description_tweet=form.cleaned_data['description_tweet'],
                        description=form.cleaned_data['description_long'],
                        hrec=form.cleaned_data['hrec'],
                        data=form.cleaned_data['data'],
                        image=form.cleaned_data['image'],
                        start=form.cleaned_data['start'],
                        end=form.cleaned_data['end'],
                        data_info=form.cleaned_data['data_info'],
                        groupId='dcd:groups:'+form.cleaned_data['title'].replace(" ", ""),
                    )
                project.save()

                property_types = get_property_types(request.session['token'])
                form = ProjectForm(choices=property_types)
                #form = ProjectForm()
                return render(request, 'bucket_new.html', {'form': form})
            else:
                print("Something went wrong with the Group...") #TODO: Deal with this
        else:
            print("Something went wrong with the Form...")  # TODO: Display message
    else:
        property_types = get_property_types(request.session['token'])
        form = ProjectForm(choices=property_types)
        #form = ProjectForm()
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

            property = new_property(project.title, project.description, project.data)
            property = create_property(request.user.thing_id, property, request.session['token'])
            if property.ok:
                print("Property created")
                propertyId = property.json()['id']
                print(propertyId)
                print(project.groupId)
                consent = new_consent([project.groupId], ['dcd:read'])
                consent = grant_consent(request.user.thing_id, propertyId, consent, request.session['token'])

                if consent.ok:
                    a = list_consent(request.user.thing_id, propertyId, request.session['token'])
                    print(a.json())
                    donation = Donation(
                        user        = request.user,
                        project     = project,
                        updates     = form.cleaned_data['updates'],
                        propertyId  = propertyId,
                    )
                    donation.save()
                else:
                    print("Something went wrong with the Consent") #TODO: Deal with this
                    print(consent.json())
            else:
                print("Something went wrong with the Property...") #TODO: Deal with this
                print(property.json())

            return render(request, 'project_view.html', {'project': project, 'form': form})
        else:
            print("Something went wrong with the Form...") #TODO: Fix this
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
        #print(property_types_list)

    return property_types_list