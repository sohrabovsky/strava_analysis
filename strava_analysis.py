import pandas as pd
import numpy as np
import plotly.graph_objects as go
pd.options.plotting.backend= 'plotly'
import datetime
import plotly.io as pio


### Importing files

df_activities= pd.read_csv('activities.csv')

df= df_activities[['Activity ID','Activity Date', 'Activity Type', 'Distance', 'Moving Time', 'Average Speed', 'Max Speed']]

outdoors= ['Run', 'Ride', 'Hike']

df= df[df['Activity Type'].isin(outdoors)]

df['Distance']= df['Distance'].astype(float)

df['Activity Date']= pd.to_datetime(df['Activity Date'])
df['Activity Date']= df['Activity Date'].dt.strftime('%Y-%m-%d')
df['Activity Date']= pd.to_datetime(df['Activity Date'])

df.set_index('Activity Date', inplace= True)

df.index.freq= pd.infer_freq(df.index)

### Moving Time Analysis

## Monthly

df_moving_time= df['Moving Time'].resample(rule= 'M').sum()

df_moving_time= df_moving_time/3600

fig= go.Figure()
fig.add_trace(go.Scatter(
    x= df_moving_time.index,
    y= df_moving_time.values,
    name= 'Moving Time'
    ))

fig.update_layout(title= 'Moving Time per Month (hrs)', template= 'ygridoff',
                  legend= dict())
pio.write_image(fig, 'moving_time_per_month.jpeg', width= 1000)

## Yearly

df_moving_time= df['Moving Time'].resample(rule= 'AS').sum()

df_moving_time= df_moving_time/3600

fig= go.Figure()
fig.add_trace(go.Bar(
    x= df_moving_time.index,
    y= df_moving_time.values,
    marker= dict(color= 'red'),
    text= df_moving_time.values,
    textposition= 'outside',
    texttemplate= '%{text:0.2f}',
    name= 'Moving Time'
    ))

fig.update_layout(title= 'Moving Time per Year (hrs)', template= 'ygridoff',
                  legend= dict(), height= 500)

pio.write_image(fig, 'moving_time_per_year.jpeg', width= 1000)
#### Run Analysis

df_runs= df[df['Activity Type'] == 'Run']
df_runs['pace']= (df_runs['Moving Time']/60)/df_runs['Distance']

## # of runs per month

df_runs_counts_monthly= df_runs['Activity ID'].resample(rule= 'M').count()
df_runs_distance_monthly= df_runs['Distance'].resample(rule= 'M').sum()


from plotly.subplots import make_subplots
fig= make_subplots(specs= [[{'secondary_y' : True}]])
fig.add_trace(go.Scatter(
    x= df_runs_counts_monthly.index,
    y= df_runs_counts_monthly.values,
    name= '# of Runs per Month'
    ), secondary_y= False)
fig.add_trace(go.Bar(
    x= df_runs_distance_monthly.index,
    y= df_runs_distance_monthly.values,
    name= 'Sum of Distance per Month (km)',
    opacity= 0.5,
    marker= dict(color= 'green')
    ), secondary_y= True)

fig.add_annotation(
        x= '2020-02-29',
        y= 10,
        text= "Corona Catastrophie",
        showarrow= True,
    )

fig.add_annotation(
        x= '2020-08-31',
        y= 4,
        text= "joining Kayson and Nada's prison started",
        showarrow= True,
    )

fig.add_annotation(
        x= '2021-09-30',
        y= 12,
        text= "Joining SnappTrip and Nada was hospitalized",
        showarrow= True,
    )

fig.update_layout(title= 'Runs per Month with Distance', template= 'ygridoff',
                  legend= dict())

pio.write_image(fig, 'run_per_month_with_dist.jpeg', width= 1500)

### Run counts yearly

df_runs_counts_yearly= df_runs['Activity ID'].resample(rule= 'AS').count()

fig= go.Figure()
fig.add_trace(go.Bar(
    x= df_runs_counts_yearly.index,
    y= df_runs_counts_yearly.values,
    marker= dict(color= 'green'),
    text= df_runs_counts_yearly.values,
    textposition= 'outside'
    ))

fig.update_layout(title= 'Runs per Year', template= 'ygridoff',
                  legend= dict(), height= 500)

pio.write_image(fig, 'run_counts_yearly.jpeg', width= 1000)

### Average Pace and Distance

df_runs_avg_pace_monthly= df_runs['pace'].resample(rule= 'M').mean()

fig= make_subplots(specs= [[{'secondary_y' : True}]])
fig.add_trace(go.Bar(
    x= df_runs_distance_monthly.index,
    y= df_runs_distance_monthly.values,
    name= 'Sum of Distance per Month (km)',
    opacity= 0.5,
    marker= dict(color= 'green')
    ), secondary_y= True)
fig.add_trace(go.Scatter(
    x= df_runs_avg_pace_monthly.index,
    y= df_runs_avg_pace_monthly.values,
    name= 'AVG pace per Month', 
    ), secondary_y= False)

fig.update_layout(title= 'Avg pace Vs sum of Distance', template= 'ygridoff',
                  legend= dict())

pio.write_image(fig, 'avg_pace_vs_dist.jpeg', width= 1500)
### Average Pace Yearly

df_runs_avg_pace_yearly= df_runs['pace'].resample(rule= 'AS').mean()

fig= go.Figure()

fig.add_trace(go.Bar(
    x= df_runs_avg_pace_yearly.index,
    y= df_runs_avg_pace_yearly.values,
    marker= dict(color= 'green'),
    text= df_runs_avg_pace_yearly.values,
    textposition= 'outside',
    texttemplate= '%{text:0.2f}',
    name= '# Avg Pace per Year'
    ))

fig.update_layout(title= 'Avg Pace per Year', template= 'ygridoff',
                  legend= dict())

pio.write_image(fig, 'avg_pace_per_year.jpeg', width= 1000)

### Distance per Year

df_runs_distance_yearly= df_runs['Distance'].resample(rule= 'AS').sum()

fig= go.Figure()
fig.add_trace(go.Bar(
    x= df_runs_distance_yearly.index,
    y= df_runs_distance_yearly.values,
    marker= dict(color= 'green'),
    text= df_runs_distance_yearly.values.astype(int),
    textposition= 'outside'
    ))

fig.update_layout(title= 'Distance per Year (km)', template= 'ygridoff',
                  legend= dict(), height= 500)

pio.write_image(fig, 'avg_dist_per_year.jpeg', width= 1000)

### Distance per Run

distance_per_run_yearly= df_runs_distance_yearly/df_runs_counts_yearly
fig= go.Figure()
fig.add_trace(go.Bar(
    x= distance_per_run_yearly.index,
    y= distance_per_run_yearly.values,
    marker= dict(color= 'green'),
    text= distance_per_run_yearly.values,
    textposition= 'outside',
    texttemplate='%{text:.2f}'
    ))

fig.update_layout(title= 'Run per Distance - Yearly (km)', template= 'ygridoff',
                  legend= dict(), height= 500)

pio.write_image(fig, 'dist_per_run_yearly.jpeg', width= 1000)

