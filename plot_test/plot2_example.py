import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash

# Data is loaded in the global state of the app, at the start. So when a user visits the app or interacts with it the data is already in memory.

app = DjangoDash('Test2')

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

transcript_list = [[1626806294000, 'saludos'], [1626759008000, 'cuento mi amor en ir al trabajo en tren'], [1626758997000, 'cuánto memoria mira trabajo por truck en transporte público'], [1626758957000, 'cuéntame Morón ir a la oficina'], [1626758948000, 'qué hora es'], [1626555886000, 'para'], [1626555875000, 'reproduce música en Spotify'], [1626555453000, 'pon ladybug name'], [1626470066000, 'cómo es el nombre verdadero de Ruth'], [1626470024000, 'cuéntanos un chiste'], [1626357532000, 'reproduce Belinda'], [1626330944000, 'pon un verano en Nueva York']]

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

app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure=fig
    ),

    html.Div([
        dcc.Markdown("""
            **Selected Points**

            Click on the points in the graph
        """),
        html.Pre(id='selected-data', style=styles['pre']),
    ]),

    html.Button(id='submit-button-state', n_clicks=0, children="Submit")
])

@app.callback(
    Output('selected-data', 'children'),
    Input('submit-button-state', 'n_clicks'),
    #Input('basic-interactions', 'selectedData'),
    State('basic-interactions', 'selectedData'),
)
def display_selected_data(n_clicks, selectedData):

    return json.dumps(selectedData, indent=2)

#def fetch data!


# Callback Functions: Automatically called when an input component's property changes in order to update some property in another component (the output!)


#KWARGS:
# callback_context : Dash Callback Context
# dash_app : DashApp model instance
# dash_app_id
# request : Django Request Object
# session_state: Dictionary of information that is unique to this user session. # Any changes made to its content are persisted as part of the session.
# user: Django User
