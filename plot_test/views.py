from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd

# Create your views here.
def plot_test(request):

    def scatter():
        x1 = [1,2,3,4]
        y1 = [5, 50, 25, 65]

        trace = go.Scatter(
            x=x1,
            y=y1
        )
        layout = dict(
            title='Static Graph',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis=dict(range=[min(y1), max(y1)])
        )

        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)

        return plot_div

    context = {
        'plot' : scatter()
    }

    return render(request, 'plot_test.html', context)


def plot_test_2(request):

    return render(request, 'plot_test_2.html')

def plot_test_3(request):

    session = request.session

    if request.method == 'POST' and 'confirm' in request.POST:
        s = request.session.get('django_plotly_dash', dict())
        print('------ POINTS HERE ------')
        print(s)
        #TODO: Render request somewhere else

    # Data:
    transcript_list = [[1626806294000, 'saludos'], [1626759008000, 'cuento mi amor en ir al trabajo en tren'],
                       [1626758997000, 'cuánto memoria mira trabajo por truck en transporte público'],
                       [1626758957000, 'cuéntame Morón ir a la oficina'], [1626758948000, 'qué hora es'],
                       [1626555886000, 'para'], [1626555875000, 'reproduce música en Spotify'],
                       [1626555453000, 'pon ladybug name'], [1626470066000, 'cómo es el nombre verdadero de Ruth'],
                       [1626470024000, 'cuéntanos un chiste'], [1626357532000, 'reproduce Belinda'],
                       [1626330944000, 'pon un verano en Nueva York']]



    context = {}

    dash_context = request.session.get('django_plotly_dash', dict()) # If session has a key with that value it returns the value associated with that key. Otherwise returns an empty dict
    # Dash context: Session with django_plotly_dash key (could be empty)
    dash_context['django_to_dash_context'] = transcript_list # Add data to session under key: django_to_dash_context. Meaning the session dictionary now has a key django_to_dash whose value are the transcripts
    request.session['django_plotly_dash'] = dash_context # Adds dash_context to the session under django_plotly_dash.

    return render(request, 'plot_test_3.html', context=context)

#KWARGS:
# callback_context : Dash Callback Context
# dash_app : DashApp model instance
# dash_app_id
# request : Django Request Object
# session_state: Dictionary of information that is unique to this user session. # Any changes made to its content are persisted as part of the session.
# user: Django User
