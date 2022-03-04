import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash

app = DjangoDash('Test3')

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}



#transcript_list = [[1626806294000, 'saludos'], [1626759008000, 'cuento mi amor en ir al trabajo en tren'], [1626758997000, 'cuánto memoria mira trabajo por truck en transporte público'], [1626758957000, 'cuéntame Morón ir a la oficina'], [1626758948000, 'qué hora es'], [1626555886000, 'para'], [1626555875000, 'reproduce música en Spotify'], [1626555453000, 'pon ladybug name'], [1626470066000, 'cómo es el nombre verdadero de Ruth'], [1626470024000, 'cuéntanos un chiste'], [1626357532000, 'reproduce Belinda'], [1626330944000, 'pon un verano en Nueva York']]

def create_figure(transcript_list):
    df = pd.DataFrame(transcript_list, columns=['Timestamp', 'Transcript'])
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
    dcc.Graph(
        id='basic-interactions',
    ),
    html.Div(id='selected-data'),
    #html.Button(id='submit-button-state', n_clicks=0, children="Submit")
])

@app.expanded_callback(
    Output('selected-data', 'children'),
    Output('basic-interactions', 'figure'),
    #Input('submit-button-state', 'n_clicks'),
    Input('basic-interactions', 'selectedData'),
    #State('basic-interactions', 'selectedData'),
)
#n_clicks,
def display_selected_data(selectedData, sesion_state=None, *args, **kwargs):
    fig = create_figure(kwargs['session_state']['django_to_dash_context'])
    #children = [html.Div(["The session context message is '%s'" % (kwargs['session_state']['django_to_dash_context'])])]

    if selectedData:
        points = len(selectedData['points'])
    else:
        points = 0

    n_points = f'Data Points Selected: {points}'
    return n_points, fig
