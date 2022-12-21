# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(id='site-dropdown',
                                    options=[{'label':'All Sites','value':'ALL'},
                                        {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                        {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                        {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                        {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'}],
                                    value='All',placeholder='Select a Launch Site',searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000,step=1000,
                                marks={0:'0',1000:'1000',3000:'3000',5000:'5000',7000:'7000',10000:'10000'},
                                value=[0,10000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[['Launch Site','class']]

    if entered_site == 'ALL':
        data = filtered_df.groupby('Launch Site').sum().reset_index()
        fig = px.pie(data, values='class', 
        names='Launch Site', 
        title='Total Successes by Site')
        return fig
    else:
        data = pd.DataFrame(filtered_df[filtered_df['Launch Site']==entered_site]['class'].value_counts())
        data.columns=['count']
        data.reset_index(inplace=True)
        fig = px.pie(data, values='count', 
        names='index', 
        title='Successes (1) and Failures (0)') 
        return fig
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(entered_site,payload_range):
    data = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_range[0],payload_range[1])]
    if entered_site == 'ALL':
        fig = px.scatter(data, x='Payload Mass (kg)', y='class',
            color = 'Booster Version Category',
            title='Success by Payload Mass, All Sites')
        return fig
    else:
        data = spacex_df[(spacex_df['Payload Mass (kg)'].between(payload_range[0],payload_range[1])) & (spacex_df['Launch Site']==entered_site)]
        fig = px.scatter(data, x='Payload Mass (kg)', y='class',
            color = 'Booster Version Category',
            title='Success by Payload Mass') 
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
