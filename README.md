## Strava Activities Data Analysis
##### Analyzing outdoor activity duration as well as quality of activities are in this notebook.You can simply change my 'activities.csv' file with yours from Strava data to plot yours plots.

##### Importing Packages and data:

```
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime

df_activities= pd.read_csv('activities.csv')
```

##### Creating Outdoor activities DataFrame based on required columns for analysis
```
df= df_activities[['Activity ID','Activity Date', 'Activity Type', 'Distance', 'Moving Time', 'Average Speed']]

outdoors= ['Run', 'Ride', 'Hike']

df= df[df['Activity Type'].isin(outdoors)]
```
##### In codes below, I created a df for suitable columns for analysis. Also, I applied some changes to columns and then set time index for it.
```
df['Distance']= df['Distance'].astype(float)

df['Activity Date']= pd.to_datetime(df['Activity Date'])
df['Activity Date']= df['Activity Date'].dt.strftime('%Y-%m-%d')
df['Activity Date']= pd.to_datetime(df['Activity Date'])
```
##### Also you can change index to datetime for ease in resampling:
```
df.set_index('Activity Date', inplace= True)

df.index.freq= pd.infer_freq(df.index)
```
##### Then, I plotted moving time to access my outdoor active duration in each month:
```
df_moving_time= df['Moving Time'].resample(rule= 'M').sum()

df_moving_time= df_moving_time/3600 #converting time to hrs

fig= go.Figure()
fig.add_trace(go.Scatter(
    x= df_moving_time.index,
    y= df_moving_time.values,
    name= 'Moving Time',
    marker= dict(color= '#655967')
    ))
max_moving_time_date= df_moving_time[df_moving_time.values == df_moving_time.values.max()].index[0]
max_moving_time_value= df_moving_time[df_moving_time.values == df_moving_time.values.max()].values[0]

fig.add_annotation(
        x= max_moving_time_date,
        y= max_moving_time_value,
        text= f'maximum moving time is {round(max_moving_time_value)} hrs',
        showarrow= True,
        bgcolor= '#98BF64',
        font= dict(color= 'white')
    )

lastmonth_moving_time_date= df_moving_time.index[-1]
lastmonth_moving_time_value= df_moving_time.values[-1]


fig.add_annotation(
        x= lastmonth_moving_time_date,
        y= lastmonth_moving_time_value,
        text= f'last month moving time is {round(lastmonth_moving_time_value)} hrs',
        showarrow= True,
        bgcolor= '#98BF64',
        font= dict(color= 'white')
    )

fig.update_layout(title= 'Moving Time per Month (hrs)',
                  template= 'plotly_white',
                  legend= dict(),
                  xaxis_title= 'Months',
                  yaxis_title= 'Hours')

fig.show()
```
![moving_time](https://github.com/sohrabovsky/strava_analysis/assets/66798323/97bddbcc-fa1d-4f54-8e3b-7830f93a590e)

##### For analysing your running activity, you can use a plotly interactive scatter plot.
##### It not only gives you flexibility to zoom over your data, but also is great tool for visualizing three metrics in time intervals as below:
###### *note that size of bubbles indicate distance of total runs in each month*
```
df_runs= df[df['Activity Type'] == 'Run'] #filter activity to run
df_runs['speed']= df_runs['Distance']/(df_runs['Moving Time']/3600) # converting speed to km/hrs

#Plot scatter chart of distance, speed, and number of runs per month

df_runs_counts_monthly= df_runs['Activity ID'].resample(rule= 'M').count()
df_runs_distance_monthly= df_runs['Distance'].resample(rule= 'M').sum()
df_runs_speed_monthly= df_runs['speed'].resample(rule= 'M').median()
size= df_runs_distance_monthly.values

fig= go.Figure()
fig.add_trace(go.Scatter(
    x= df_runs_counts_monthly.index,
    y= df_runs_counts_monthly.values,
    mode= 'markers',
    marker= dict(
    size= size,
    color= df_runs_speed_monthly.values,
    sizemode= 'area',
    showscale= True,
    colorbar= dict(title= 'Speed'),
    colorscale= 'speed',
    ),
    name= '# of Runs per Month')
    )
fig.add_vline(x= '2018-09-15', line_dash= 'dash', line_color= 'green', name= 'Start Running')
fig.add_annotation(
        x= '2018-09-15',
        y= 25,
        text= "Start Running",
        showarrow= False,
        bgcolor= '#98BF64',
        font= dict(color= 'white')
    )


fig.add_vline(x= '2020-02-15', line_dash= 'dash', line_color= 'red', name= 'Corona Catastrophie')
fig.add_annotation(
        x= '2020-02-29',
        y= 22,
        text= "Corona Catastrophie",
        showarrow= False,
        bgcolor= '#655967',
        font= dict(color= 'white')
    )

fig.add_vline(x= '2020-08-15', line_dash= 'dash', line_color= 'orange', name= 'My personal life 1st big issue')
fig.add_annotation(
        x= '2020-08-31',
        y= 25,
        text= "My personal life 1st big issue",
        showarrow= False,
        bgcolor= '#655967',
        font= dict(color= 'white')
    )
fig.add_vline(x= '2021-09-15', line_dash= 'dash', line_color= 'yellow', name= 'My personal life 2nd big issue')
fig.add_annotation(
        x= '2021-09-30',
        y= 22,
        text= "My personal life 2nd big issue",
        showarrow= False,
        bgcolor= '#655967',
        font= dict(color= 'white')
    )

fig.update_layout(title= 'Monthly Runs',
                  template= 'plotly_white',
                  legend= dict(),
                  xaxis_title= 'Months',
                  yaxis_title= '# of Runs')

fig.show()
```
![scatter_plot](https://github.com/sohrabovsky/strava_analysis/assets/66798323/61046dd6-82bd-45fa-91e1-7eb6fc981a31)

