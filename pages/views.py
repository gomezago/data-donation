from django.shortcuts import render

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