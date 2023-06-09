from zipfile import ZipFile
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import io
import json
import os
import itertools
import time
from datetime import datetime
from utils.bucket_functions import *
import time
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import xml.etree.ElementTree as ET

def s_to_hours(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return ("%d:%d:%d" % (hours, minutes, seconds))

def ms_to_hours(millis):
    seconds, milliseconds = divmod(millis, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return ("%d:%d:%d" % (hours, minutes, seconds))

def delta_to_time(time_delta):
    seconds = time_delta.total_seconds()
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return ("%d:%d:%d" % (hours, minutes, seconds))

def delta_to_hour(time_delta):
    seconds = time_delta.total_seconds()
    hours = seconds / 3600
    return hours

def get_activity_data(file_names, files):
    activity_path = [file for file in file_names if 'DI_CONNECT/DI-Connect-Fitness/' and 'summarizedActivities' in file]

    if activity_path:
        d = json.loads(files[activity_path[0]])

        activity_list = []

        for item in d[0]['summarizedActivitiesExport']:
            if item['beginTimestamp'] > 1672488000000:
                if "avgHr" in item:
                    a_data = {}
                    a_data['timestamp'] = item['beginTimestamp']
                    a_data['date'] = datetime.datetime.fromtimestamp(item['beginTimestamp'] / 1000.0).strftime("%Y-%m-%d")
                    a_data['date_time'] = datetime.datetime.fromtimestamp(item['beginTimestamp'] / 1000.0)  # .strftime("%Y-%m-%d")
                    a_data['startTimeGMT'] = item['beginTimestamp']
                    a_data['startTime'] = item['startTimeLocal']
                    a_data['startHour'] = int(datetime.datetime.fromtimestamp(item['startTimeLocal'] / 1000.0).strftime("%H"))
                    a_data['startHourMinuteLocal'] = datetime.datetime.fromtimestamp(item['startTimeLocal'] / 1000.0).strftime("%Y-%m-%d %H:%M")
                    a_data['duration'] = int(item['duration'] / 60000)
                    a_data['duration_hours'] = ms_to_hours(item['duration'])
                    a_data['avgHR'] = item['avgHr']
                    a_data['maxHR'] = item['maxHr']
                    a_data['type'] = item['activityType']
                    a_data['sport'] = item['sportType']

                    a_data['text'] = (
                        'Activity: ' + a_data['sport'] + '<br>Duration: ' + str(a_data['duration_hours']) + '<br>Average HR: ' +
                        str(a_data['avgHR']) + '<br>Max HR:' + str(a_data['maxHR']) + '<br>'
                    )
                    activity_list.append(a_data)

        activity_df = pd.DataFrame(activity_list)

    else:
        activity_df = pd.DataFrame(columns=['timestamp','date', 'date_time', 'startTimeGTM', 'startTime', 'startHour', 'startHourMinuteLocal', 'duration', 'duration_hours', 'avgHR', 'maxHR', 'type', 'sport', 'text'])
    return activity_df

def get_sleep_data(file_names, files):
    sleep_path = [file for file in file_names if 'DI_CONNECT/DI-Connect-Wellness/' and 'sleepData' in file if '2023' in file]

    if sleep_path:
        sleep_list = []

        for f in sleep_path:

            d = json.loads(files[f])

            for item in d:
                if item['calendarDate'] > "2022-12-31":
                    sleep_data = {}
                    sleep_data['timestamp'] = int(time.mktime(pd.to_datetime(item['sleepStartTimestampGMT']).timetuple()) * 1000)
                    sleep_data['date'] = item['calendarDate']
                    sleep_data['start_time'] = pd.to_datetime(item['sleepStartTimestampGMT'])
                    sleep_data['end_time'] = pd.to_datetime(item['sleepEndTimestampGMT'])
                    sleep_data['deep'] = item['deepSleepSeconds'] / 3600
                    sleep_data['light'] = item['lightSleepSeconds'] / 3600
                    sleep_data['awake'] = item['awakeSleepSeconds'] / 3600
                    sleep_data['other'] = item['unmeasurableSeconds'] / 3600
                    sleep_data['duration'] = (item['deepSleepSeconds'] + item['lightSleepSeconds'] + item['awakeSleepSeconds'] + item['unmeasurableSeconds']) / 3600
                    sleep_data['duration_hours'] = s_to_hours(item['deepSleepSeconds'] + item['lightSleepSeconds'] + item['awakeSleepSeconds'] + item['unmeasurableSeconds'])

                    sleep_data['text'] = (
                                'Start Time: ' + sleep_data['start_time'].strftime('%H:%M') + '<br>End Time: ' +
                                sleep_data['end_time'].strftime('%H:%M') +
                                '<br>Duration: ' + str(sleep_data['duration_hours']) + '<br>')

                    sleep_list.append(sleep_data)

        sleep_df = pd.DataFrame(sleep_list)
    else:
        sleep_df = pd.DataFrame(columns=['timestamp', 'date', 'start_time', 'end_time', 'deep', 'light', 'awake', 'other', 'duration', 'duration_hours', 'text'])

    return sleep_df


def get_hr_data(file_names, files):
    hr_path = [file for file in file_names if 'DI_CONNECT/DI-Connect-User/UDSFile' in file if '2023' in file]

    if hr_path:
        hr_list = []

        for f in hr_path:
            d = json.loads(files[f])
            for item in d:
                item_year = datetime.datetime.strptime(item['calendarDate']['date'], '%b %d, %Y %I:%M:%S %p').date().year
                if item_year > 2022:
                    if 'restingHeartRateTimestamp' in item:
                        if 'minHeartRate' in item:
                            hr_data = {}
                            hr_data['timestamp'] = int(time.mktime(pd.to_datetime(item['restingHeartRateTimestamp']).timetuple()) * 1000)
                            hr_data['date'] = datetime.datetime.strptime(item['restingHeartRateTimestamp'],'%b %d, %Y %I:%M:%S %p').strftime("%Y-%m-%d")
                            hr_data['minHR'] = item['minHeartRate']
                            hr_data['maxHR'] = item['maxHeartRate']
                            hr_data['restHR'] = item['restingHeartRate']
                            hr_data['text'] = (
                                'Date: ' + hr_data['date'] + '<br>Resting HR: ' + str(hr_data['restHR']) + '<br>Max HR: ' + str(hr_data['maxHR']) + 'br'
                            )

                            hr_list.append(hr_data)

        hr_df = pd.DataFrame(hr_list)
    else:
        hr_df = pd.DataFrame(columns=['timestamp', 'date', 'minHR', 'maxHR', 'restHR', 'text'])

    return hr_df

def parse_zip(file):
    zip_file = ZipFile(file)

    record_list = []
    workout_list = []
    for name in zip_file.namelist():
        if 'cda' not in name and 'route' not in name:
            f = zip_file.open(name)
            tree = ET.parse(f)
            root = tree.getroot()
            record_list = [x.attrib for x in root.iter('Record')]
            workout_list = [x.attrib for x in root.iter('Workout')]

    # To Date Time
    record_df = pd.DataFrame(record_list)
    for col in ['creationDate', 'startDate', 'endDate']:
        record_df[col] = pd.to_datetime(record_df[col], errors = 'coerce')

    # Shorter Observation Names
    record_df['type'] = record_df['type'].str.replace('HKQuantityTypeIdentifier', '')
    record_df['type'] = record_df['type'].str.replace('HKCategoryTypeIdentifier', '')
    return record_df, workout_list

def get_sleep_record(record_data):

    sleep_data = record_data[(record_data['type'] == "SleepAnalysis") & (record_data['startDate'].dt.year > 2022)]

    if sleep_data.empty:

        sleep_df = pd.DataFrame(
            columns=['timestamp', 'date', 'start_time', 'end_time', 'deep', 'light', 'awake', 'other', 'duration', 'duration_hours',
                     'text'])

    else:
        sleep_data['timestamp'] = sleep_data['startDate'].apply(lambda x: int(time.mktime(pd.to_datetime(x).timetuple()) * 1000))

        sleep_data['value'] = sleep_data['value'].str.replace('HKCategoryValueSleepAnalysis', '')

        sleep_data.rename(columns={'startDate': 'start_time'}, inplace=True)
        sleep_data.rename(columns={'endDate': 'end_time'}, inplace=True)

        sleep_data['date'] = record_data['creationDate'].dt.strftime('%Y-%m-%d')

        sleep_data['duration_lambda'] = sleep_data['end_time'] - sleep_data['start_time']
        sleep_data['duration_hours'] = sleep_data['duration_lambda'].apply(delta_to_time)
        sleep_data['duration'] = sleep_data['duration_lambda'].apply(delta_to_hour)

        hover_text = []

        for index, row in sleep_data.iterrows():
            hover_text.append(('Start Time : {start}<br>' + 'End Time : {end}<br>' + 'Duration : {duration}<br>')
                              .format(start=row['start_time'].strftime('%H:%M'), end=row['end_time'].strftime('%H:%M'),
                                      duration=row['duration_hours'], ))

        sleep_data['text'] = hover_text
        sleep_df = sleep_data

    return sleep_df

def get_hr_record(record_data):

    hr_data = record_data[(record_data['type'] == "HeartRate") & (record_data['startDate'].dt.year > 2022)]
    if hr_data.empty:
        hr_agg = pd.DataFrame(columns=['timestamp','date', 'minHR', 'maxHR', 'restHR', 'text'])
    else:
        hr_data['value'] = hr_data['value'].astype(float).astype(int)

        hr_agg_data = hr_data.groupby(hr_data['startDate'].dt.date).agg({'value': ['mean', 'min', 'max']}).reset_index()
        hr_agg_data.columns = hr_agg_data.columns.droplevel(0)

        hr_agg_data = hr_agg_data.rename(columns={'' :'date', 'mean' : 'minHR', 'min' : 'restHR', 'max' : 'maxHR'})
        hr_agg_data['timestamp'] = hr_agg_data['date'].apply(lambda x: int(time.mktime(pd.to_datetime(x).timetuple()) * 1000))

        hover_text = []

        for index, row in hr_agg_data.iterrows():
            hover_text.append(('Date : {date}<br>' + 'Resting HR : {restHR}<br>' + 'Max HR : {maxHR}<br>')
                       .format(date=row['date'], restHR=row['restHR'], maxHR=row['maxHR'], ))
        hr_agg_data['text'] = hover_text
        hr_agg = hr_agg_data

    return hr_data, hr_agg


def get_hr(hr_data, start, end):
    hr_data = hr_data[hr_data["startDate"] >= start]
    hr_data = hr_data[hr_data["startDate"] <= end]

    mean_hr = hr_data['value'].mean()
    max_hr = hr_data['value'].max()

    return mean_hr, max_hr

def get_activity(workout_list, hr_data):
    activity_list = []

    for item in workout_list:
        if pd.to_datetime(item['startDate']).year > 2022:
            if item:
                hr_mean, hr_min = get_hr(hr_data, item['startDate'], item['endDate'])
                a_data = {}
                a_data['timestamp'] = int(
                    time.mktime(pd.to_datetime(item['startDate']).timetuple()) * 1000)
                a_data['date'] = pd.to_datetime(item['startDate']).strftime("%Y-%m-%d")
                a_data['startTime'] = item['startDate']
                a_data['startHour'] = int(pd.to_datetime(item['startDate']).hour)
                a_data['endTime'] = item['endDate']
                a_data['duration'] = int(float(item['duration']))
                a_data['duration_hours'] = ms_to_hours(int(float(item['duration'])))
                a_data['avgHR'] = hr_mean
                a_data['maxHR'] = hr_min
                a_data['sport'] = item['workoutActivityType'].replace('HKWorkoutActivityType', '')

                a_data['text'] = (
                        'Activity: ' + a_data['sport'] + '<br>Duration: ' + str(
                    a_data['duration_hours']) + '<br>Average HR: ' +
                        str(a_data['avgHR']) + '<br>Max HR:' + str(a_data['maxHR']) + '<br>'
                )

                activity_list.append(a_data)

    if  not activity_list:
        activity_df = pd.DataFrame(
            columns=['timestamp','date', 'date_time', 'startTime', 'startHour', 'startHourMinuteLocal',
                     'duration', 'duration_hours', 'avgHR', 'maxHR', 'type', 'sport', 'text'])

    else:
        activity_df = pd.DataFrame(activity_list)

    return activity_df

def create_sleep_dict(sleep_df):

    sleep_donation = sleep_df[['timestamp','date', 'start_time', 'end_time', 'duration']]

    # Date: String
    sleep_donation['start_time'] = sleep_donation['start_time'].astype(str)
    sleep_donation['end_time'] = sleep_donation['end_time'].astype(str)
    sleep_donation['duration'] = sleep_donation['duration'].astype(float)

    sleep_array = sleep_donation.to_numpy().tolist()
    return sleep_array

def create_hr_dict(hr_df):

    hr_donation = hr_df[['timestamp','date', 'minHR', 'maxHR', 'restHR']]

    # Date: String
    hr_donation['date'] = hr_donation['date'].astype(str)

    hr_array = hr_donation.to_numpy().tolist()
    return hr_array

def create_act_dict(act_df):

    act_donation = act_df[['timestamp','date', 'startTime', 'duration', 'avgHR', 'maxHR', 'sport']]

    # Date: String
    act_donation['date'] = act_donation['date'].astype(str)
    act_donation['startTime'] = act_donation['startTime'].astype(str)
    act_donation['duration'] = act_donation['duration'].astype(float)

    #act_dict = act_donation.to_dict('records')
    act_array = act_donation.to_numpy().tolist()
    return act_array

def create_activity_plot(activity_df, hr_df, sleep_df, last_m_date):
    pio.templates.default = "plotly_white"

    def create_plot():
        fig = make_subplots(rows=3, cols=1,
                            subplot_titles=("Physical Activity", "Sleep Duration", "Resting Heart Rate",),
                            shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.7, 0.25, 0.25])

        fig.append_trace(
            go.Scatter(x=list(hr_df.date), y=list(hr_df.restHR), hovertext=hr_df.text, mode='markers',
                       marker_symbol='line-ew-open', name='', showlegend=False), row=3, col=1
        )

        sport_types = activity_df['sport'].unique()
        sport_data = {sport: activity_df.query("sport == '%s'" % sport) for sport in sport_types}

        sizeref = 2. * max(activity_df['duration'], default=5) / (40 ** 2)

        for sport_type, sport in sport_data.items():
            fig.append_trace(go.Scatter(x=sport['date'], y=sport['startHour'], name=sport_type, text=sport['text'],
                                        marker_size=sport['duration'], mode='markers', marker_symbol='circle',
                                        marker=dict(sizemode='area', sizeref=sizeref), ), row=1, col=1)

        fig.append_trace(
            go.Bar(x=list(sleep_df.date), y=sleep_df.duration, name='', showlegend=False, hovertext=sleep_df.text), row=2,
            col=1)

        fig.update_layout(height=600, width=600, title_text="", margin=dict(l=5,r=5,t=5,b=5))

        fig.update_layout(

            xaxis=dict(

                rangeselector=dict(
                    buttons=list([

                        dict(count=1,
                             label="1D",
                             step="day",
                             stepmode="backward"),

                        dict(count=7,
                             label="1W",
                             step="day",
                             stepmode="backward"),

                        dict(count=1,
                             label="1M",
                             step="month",
                             stepmode="backward"),

                        dict(count=3,
                             label="3M",
                             step="month",
                             stepmode="backward"),

                    ])
                ),
                rangeslider=dict(visible=False),
                type="date"
            )

        )

        fig.update_layout(xaxis_showticklabels=True,
                          xaxis2_showticklabels=True,
                          xaxis_rangeslider_visible=False,
                          xaxis2_rangeslider_visible=False,
                          xaxis3_rangeslider_visible=True,
                          xaxis_type="date",)
        fig.update_layout(legend=dict(
            orientation = 'h',
            yanchor = "top",
            y = 0.99,#1.02,
            xanchor = "left",
            x = 0.01,#1
            font=dict(
                size=9,
            ),
        ))

        fig['layout']['yaxis']['title'] = 'Time of the Day'
        fig['layout']['yaxis2']['title'] = 'Total Hours'
        fig['layout']['yaxis3']['title'] = 'Beats per Min'

        fig.update_xaxes(range=[hr_df.date.min(), hr_df.date.max()], rangeslider_thickness = 0.05)

        fig.add_vline(x=last_m_date, line_width=1, line_dash="dash", line_color="red")

        fig.update_layout(showlegend=True)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div
    return create_plot()


