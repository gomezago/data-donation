from django.shortcuts import render

# Create your views here.
def pages_index(request):
    return render(request, 'pages_index.html')