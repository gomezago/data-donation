from django.shortcuts import render
from bucket_view.models import Project

# Create your views here.
def pages_index(request):
    return render(request, 'pages_index.html')

def pages_about(request):
    return render(request, 'pages_about.html')

def pages_questions(request):
    return render(request, 'pages_questions.html')

def pages_publications(request):
    return render(request, 'pages_publications.html')

def pages_privacy(request):
    return render(request, 'pages_privacy.html')

def pages_terms(request):
    return render(request, 'pages_terms.html')

def pages_instructions(request, pk):

    project = Project.objects.get(pk=pk)
    return render(request, 'pages_instructions.html', {'project': project})

def pages_extensions(request):
    return render(request, 'pages_extensions.html')

def error_404(request, exception):
        data = {}
        return render(request, 'pages_404.html', data)


def error_403(request, exception):
    data = {}
    return render(request, 'pages_403.html', data)


def error_400(request, exception):
    data = {}
    return render(request, 'pages_400.html', data)


def error_500(request):
    return render(request, 'pages_500.html', status=500)