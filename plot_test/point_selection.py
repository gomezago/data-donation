import json
import base64
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
import pandas as pd
from django_plotly_dash import DjangoDash
from utils.bucket_functions import get_property_media

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('PointSelection', external_stylesheets=external_stylesheets)
pio.templates.default = "plotly_white"

def create_figure(transcript_list):
    df = pd.DataFrame(transcript_list, columns=['Timestamp', 'Path', 'Transcript'])
    df['DateTime'] = pd.to_datetime(df['Timestamp'], unit='ms')
    df['DateString'] = df['DateTime'].dt.strftime("%m/%d/%Y, %H:%M")
    df['Hour'] = df['DateTime'].dt.hour

    # Custom data to select to Hover, Click, and Selection Events
    fig = px.scatter(df, x="DateTime", y="Hour", custom_data=["Timestamp", "DateString", "Path"], opacity=0.5,
    labels={
                         "DateTime" : "Date",
                         "Hour": "Hour",
                     },
                         hover_name="DateTime", hover_data={'DateTime':False, 'Hour':False, 'Transcript':True, 'DateString' : True, },
                     )

    fig.update_layout(clickmode='event+select', margin=dict(l=20, r=20, t=20, b=20),)
    fig.update_traces(marker_size=10, selector=dict(mode='markers', color='red'))
    fig.update_traces(hovertemplate='<b>Transcript:</b> %{customdata[3]} <br><b>Date:</b> %{customdata[1]}<br>')

    return fig


app.layout = html.Div([
    html.Div(id='audio-player', children=[]),
    dcc.Graph(id='basic-interactions',),
],style={'marginBottom': 0, 'marginTop': 0,})

@app.expanded_callback(
    Output('audio-player', 'children'),
    Input('basic-interactions', 'hoverData'),
)

def reproduce_on_click(hoverData, session_state=None, *args, **kwargs):
    if session_state is None:
        raise NotImplementedError("Missing session state")

    token = session_state.get('token', {})
    thing = session_state.get('thing_id', {})
    property = session_state.get('property', {})
    type = 'speech-record-mp3'

    if hoverData:
        if 'customdata' in hoverData['points'][0].keys():
            timestamp = hoverData['points'][0]['customdata'][0]
            a = get_property_media(thingId=thing, propertyId=property, timestamp=timestamp, dimension=type, token=token)
            encoded = base64.b64encode(a.content).decode('utf8')
            string = f'data:audio/mpeg;base64,{encoded}'

            audio = html.Div(children=[
                html.Audio(autoPlay=True, preload='auto', controls=True, src=string)
            ])
        else:
            audio = html.Div([])
    else:
        audio = html.Div([])
    return audio

@app.expanded_callback(
    Output('basic-interactions', 'figure'),
    Input('basic-interactions', 'selectedData'),
)

def display_selected_data(selectedData, session_state=None, *args, **kwargs):

    if session_state is None:
        raise NotImplementedError("Missing session state")
    initial_points = session_state.get('django_to_dash_context', {})
    fig = create_figure(initial_points)

    if selectedData:
        session_state['selected_points'] = selectedData
        x = [d['x'] for d in selectedData['points']]
        y = [d['y'] for d in selectedData['points']]
        fig.add_trace(go.Scatter(x=x, y=y, name='Selected', mode='markers',
                                 marker_symbol='x',
                                 marker_size=10))
    else:
        session_state['selected_points'] = {}
    return fig

