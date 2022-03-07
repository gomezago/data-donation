import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
import pandas as pd
from django_plotly_dash import DjangoDash

app = DjangoDash('PointSelection')
pio.templates.default = "plotly_white"


def create_figure(transcript_list):
    df = pd.DataFrame(transcript_list, columns=['Timestamp', 'Path', 'Transcript'])
    df['DateTime'] = pd.to_datetime(df['Timestamp'], unit='ms')
    df['Hour'] = df['DateTime'].dt.hour

    # Custom data to select to Hover, Click, and Selection Events
    fig = px.scatter(df, x="DateTime", y="Hour", custom_data=["Timestamp"],
    labels={
                         "DateTime" : "Date",
                         "Hour": "Hour",
                     },
                         hover_name="DateTime", hover_data={'DateTime':False, 'Hour':False, 'Transcript':True,},
                     )

    fig.update_layout(clickmode='event+select')
    fig.update_traces(marker_size=20)
    fig.update_traces(hovertemplate='<b>Transcript:</b> %{customdata[1]} <br><b>Date:</b> %{hovertext}')

    return fig


app.layout = html.Div([
    dcc.Graph(id='basic-interactions'),
    html.Div(id='selected-data', style={
        'font-family': 'Lora',
    }),])

@app.expanded_callback(
    Output('selected-data', 'children'),
    Output('basic-interactions', 'figure'),
    Input('basic-interactions', 'selectedData'),
)

def display_selected_data(selectedData, session_state=None, *args, **kwargs):

    if session_state is None:
        raise NotImplementedError("Missing session state")
    initial_points = session_state.get('django_to_dash_context', {})
    fig = create_figure(initial_points)

    if selectedData:
        points = len(selectedData['points'])
        session_state['selected_points'] = selectedData
    else:
        points = 0
        session_state['selected_points'] = {}
    n_points = f'Selected Points: {points}'
    return n_points, fig
