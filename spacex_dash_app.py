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

# Extract unique launch sites
unique_launch_sites=spacex_df['Launch Site'].unique()

# Create a list of dictionaries
dropdown_options = [{'label': site, 'value': site} for site in unique_launch_sites]

# add the "All site" option
dropdown_options.insert(0,{'label': 'All Sites','value':'All'})

min_value = 2500
max_value = 7500
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=dropdown_options,
                                             value='All',
                                             placeholder='Select a Launch Site here',
                                             searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks={0:'0',
                                                       2500:'2500',
                                                       5000:'5000',
                                                       7500:'7500',
                                                       10000:'10000'
                                                       },
                                                value=[min_value, max_value]       
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    success_df = spacex_df[spacex_df['class']==1]
    # print('entered_site ',entered_site)
    if entered_site == 'All':
        fig = px.pie(success_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        filtered_df_counts = filtered_df['class'].value_counts().reset_index()
        filtered_df_counts.columns=['class','Count']
        fig = px.pie(filtered_df_counts, values='Count', 
        names='class', 
        title='Total Success Launches For Site {}'.format(entered_site))
        # title='Total Success Launches For Site ')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'),Input(component_id='payload-slider', component_property='value')])
# @app.callback([Output(component_id='plot1', component_property='children'),
#                Output(component_id='plot2', component_property='children')],
#                [Input(component_id='region', component_property='value'),
#                 Input(component_id='year', component_property='value')])
def get_scatter_chart(entered_site, selected_payload):
    if entered_site=='All':
        filter_cond = (spacex_df['Payload Mass (kg)']>=selected_payload[0]) & (spacex_df['Payload Mass (kg)']<=selected_payload[1])
        filtered_df = spacex_df[filter_cond]
        fig = px.scatter(filtered_df,x='Payload Mass (kg)', y='class',color='Booster Version Category',
                         title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        filter_cond = ((spacex_df['Launch Site']==entered_site) & (spacex_df['Payload Mass (kg)']>=selected_payload[0]) & (spacex_df['Payload Mass (kg)']<=selected_payload[1]))
        filtered_df = spacex_df[filter_cond]
        fig = px.scatter(filtered_df,x='Payload Mass (kg)', y='class',color='Booster Version Category',
                         title='Correlation between Payload and Success for site {}'.format(entered_site))
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
