from django.shortcuts import render
import requests
from .forms import ProjectForm, DonateForm
from .models import Project, Donation
from utils.bucket_functions import new_group, new_consent, new_property, create_group, create_property, grant_consent, list_consent

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
                form = ProjectForm()
                return render(request, 'bucket_new.html', {'form': form})
            else:
                print("Something went wrong with the Group...") #TODO: Deal with this
        else:
            print("Something went wrong with the Form...")  # TODO: Display message
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

