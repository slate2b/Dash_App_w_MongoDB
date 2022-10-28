import dash_leaflet as dl
from dash import dcc
from dash import html
from dash import dash_table as dt
import plotly.express as px
from dash import Dash
from dash.dependencies import Input, Output, State
import base64
import pandas as pd

# Importing the animal_shelter CRUD Module
from animal_shelter import AnimalShelter

############################################################################################
#
#  This project is a Client-Server Dashboard Application which follows the Model View
#  Controller (MVC) Software Design Pattern.  It uses the RESTful protocol for additional
#  utility and security.  The application includes a database and a client-facing web
#  application dashboard which allows users to interact with the data through filter
#  options and a data table.  The dashboard also provides data visualization through a
#  pie chart and a geolocation chart which update based on the user’s interactions with
#  the filters and the data table.  I originally created the sketch of this application
#  in my Client-Server Application Development class at Southern New Hampshire University,
#  but this version includes several changes.
#
#  The application was designed for a hypothetical client named Grazioso Salvare,
#  a company which trains rescue animals.  The client needed to be able to quickly
#  analyze data from local animal shelters to identify potential candidates for rescue
#  training.
#
#  The original project used a conventional MongoDB database as the data model with the
#  view and controller components implemented in Jupyter Notebook.  For this implementation,
#  however, I switched to MongoDB Atlas for the data model and switched to all Python source
#  code for the view and controller (not Jupyter).
#
#  This project includes the following modules, libraries, components, widgets, etc:
#
#    - CRUD module (animal_shelter.py) which handles the interactions between the dashboard
#      and the data model
#    - The source code for the dashboard (dashboard.py)
#    - MongoDB Atlas database
#    - Dash Framework
#    - Pandas DataFrame
#    - Dash DataTable
#    - Dash-Leaflet Geolocation Chart
#    - Plotly Express Pie Chart
#
#  The CRUD module and dashboard could be easily adapted for use in any number of client-
#  server applications.
#
#  Credit for the company logo and idea for the project go to the Computer Science Program
#  at Southern New Hampshire University (SNHU).  Thank you!
#
############################################################################################


###########################
# Data Manipulation / Model
###########################

# Hard-coding the username and password into the current implementation
username = "gsUser"
password = "gsUserPass1"

# Creating a AnimalShelter (CRUD class) object
shelter = AnimalShelter(username, password)

# Calling the read_all method from the CRUD module and creating a pandas DataFrame
df = pd.DataFrame.from_records(shelter.read_all({}))


#########################
# Dashboard Layout / View
#########################
app = Dash(__name__)

# Loading image for dashboard
image_filename = 'Grazioso Salvare Logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# App layout for the dashboard
app.layout = html.Div([

    #
    # Page Header
    html.Div([
        html.Br(),
        html.Center(html.B(html.H1('Rescue Animal Interactive Dashboard'))),
        html.Center(html.H4('Developer: Thomas Vaughn')),
        html.Br()
    ]),

    #
    # Company Logo
    html.Div([
        # Displaying the image loaded / encoded above
        html.A(html.Center(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                                    style={'width': '300px', 'height': '300px'})),
               # Adding a link to the logo which routes to my github profile
               href='https://github.com/slate2b'
               ),
        html.Br(), html.Hr()
    ]),

    #
    # Instructions for the dashboard user - RadioItems
    html.Div([
        html.Br(),
        html.Center(html.H2('Select a type of rescue to filter results:')),
    ]),

    #
    # RadioItems to filter results in the data table and charts
    html.Div([
        html.Center(
            dcc.RadioItems(
                id='radio-items-id',
                options=[
                    {'label': 'Water Rescue', 'value': 1},
                    {'label': 'Mountain Rescue', 'value': 2},
                    {'label': 'Disaster Rescue', 'value': 3},
                    {'label': 'Reset', 'value': 4}
                ],
                labelStyle={'display': 'inline-block'}
            )
        )
    ]),

    #
    # Instructions for the dashboard user - Selecting Rows on the Data Table
    html.Div([
        html.Br(), html.Hr(), html.Br(),
        html.Center(html.H2('Data from Local Animal Shelters')),
        html.Center(html.P('Select an individual animal by selecting the corresponding row, aka the circle on the left:')),
        html.Br()
    ]),

    #
    # Dash DataTable
    html.Div([
        dt.DataTable(
            id='datatable-id',
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
            ],
            style_cell={'minWidth': '100px', 'width': '180px', 'maxWidth': '200px',
                        'overflow': 'hidden', 'textOverflow': 'ellipsis',
                        'padding': '8px'},
            data=df.to_dict('records'),
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable=False,
            row_selectable="single",
            row_deletable=False,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=10
        ),
        html.Br(), html.Br(), html.Hr(), html.Br()
    ]),

    #
    # Instructions for the dashboard user - Geolocation Chart
    html.Div([
        html.Center(html.H2('Geolocation Chart')),
        html.Center(html.P('Displays the location of the selected animal.')),
        html.Br()
    ]),

    #
    # Geolocation Chart (map)
    html.Div([
        html.Center(
            id='map-id',
            className='col s12 m6',
        ),
        html.Br(), html.Br(), html.Hr(), html.Br()
    ]),

    #
    # Instructions for the dashboard user - Pie Chart
    html.Div([
        html.Center(html.H2('Animal Breeds')),
        html.Center(html.P('Visualizes the percentage of breeds for the data.  If data has been filtered, pie chart will reflect filtered data.')),
        html.Br()
    ]),

    #
    # Pie Chart
    html.Div([
        html.Center(
            id='graph-id',
            className='col s12 m6',
        ),
        html.Br(), html.Br(), html.Br()
    ]),

    #
    # Dashboard Footer
    html.Div([
        html.Center(html.P('Developed by: Thomas Vaughn')),
        html.Br()
    ])
])


#############################################
# Interaction Between Components / Controller
#############################################

# ----------------------------------------------------------------------------------------------
# This callback returns data frame data and columns based on radio item selections from the user
# and returns the selected row to the top row displayed in the data table
# ----------------------------------------------------------------------------------------------
@app.callback([Output('datatable-id', 'data'),
               Output('datatable-id', 'columns'),
               Output('datatable-id', 'selected_rows')],
              [Input('radio-items-id', 'value')])
def update_dashboard(filter_type):

    # Default will include all records
    df = pd.DataFrame(list(shelter.read_all({})))

    # If user clicks Water Rescue
    if (filter_type == 1):
        df = pd.DataFrame(list(shelter.read_all({
            "animal_type": "Dog",
            "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": {"$gte": 26},
            "age_upon_outcome_in_weeks": {"$lte": 156}})))

    # If user clicks Mountain Rescue
    elif (filter_type == 2):
        df = pd.DataFrame(list(shelter.read_all({
            "animal_type": "Dog",
            "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog",
                              "Siberian Husky", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26},
            "age_upon_outcome_in_weeks": {"$lte": 156}})))

    # If user clicks Distaster Rescue
    elif (filter_type == 3):
        df = pd.DataFrame(list(shelter.read_all({
            "animal_type": "Dog",
            # NOTE: Using breed name 'Doberman Pinsch' to match breed name in data set
            "breed": {"$in": ["Doberman Pinsch", "German Shepherd", "Golden Retriever",
                              "Bloodhound", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 20},
            "age_upon_outcome_in_weeks": {"$lte": 300}})))

    # If user clicks reset
    elif (filter_type == 4):
        df = pd.DataFrame(list(shelter.read_all({})))

    # Set columns to return
    columns = [{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]

    # Set data to return based on conditional logic above
    data = df.to_dict('records')

    # Reset the selected row to the first row
    row = [0]

    # Return the data and columns based on user's filter radio item selection
    return (data, columns, row)


# -------------------------------------------------------------------------------------------
# This callback returns an updated pie chart based on selections and filters in the datatable
# -------------------------------------------------------------------------------------------
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', 'data')])
def update_graphs(viewData):
    # Dataframe used for the Pie Chart based on datatable input
    df = pd.DataFrame.from_dict(viewData)

    # The breed column from the data frame
    breed_data = df['breed']

    # Converting the data from the breed column to a set. This will filter the results to distinct values.
    # Using .array to access the data from the series
    breed_set = set(breed_data.array)

    # Converting the set to a list data structure
    breed_list = list(breed_set)

    # Creating a list to hold values for the pie chart
    breed_values = []

    # Creating an iterator variable and assigning -1 for use in the loop below
    i = -1

    # Loop through the breeds in breed_list to calculate values for the pie chart
    for breed in breed_list:

        # Increment the iterator variable
        i += 1

        # Create variable to count the number of the current breed and assign with zero
        breed_count = 0

        # Loop through all values in breed_data
        for j in breed_data:

            # If the current value matches the breed we're currently counting...
            if j == breed:
                # Increment the breed count
                breed_count += 1

        # After looping through the current breed, add the breed count to the breed values list
        breed_values.append(breed_count)

    # Creating the pie chart
    fig=px.pie(df, values=breed_values, names=breed_list)

    # Configuring the pie chart (especially useful when dealing with many buckets of data)
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    # Return the updated pie chart as a dcc.Graph
    return dcc.Graph(figure=fig)


# ---------------------------------------------------------------------------------------------------
# This callback returns an updated geolocation chart based on selections and filters in the datatable
# ---------------------------------------------------------------------------------------------------
@app.callback(
    Output('map-id', 'children'),
    [Input('datatable-id', 'data'), Input('datatable-id', 'selected_rows')]
)
def update_map(viewData, selectedRows):

    # Dataframe used for the Geolocation Chart based on datatable input
    df = pd.DataFrame.from_dict(viewData)

    # List of row positions for all selected rows. Current implementation only allows single row.
    selected_rows = selectedRows

    # If no rows currently selected, geolocation defaults to the data from the top row of the dataframe
    # NOTE: If filtered, the geolocation chart will update based on the top row of the filtered dataframe
    if not selectedRows:
        selected_rows = [0]

    # Creating variables for data to be displayed in the marker's tooltip and popup based off selected row
    breed = df.iloc[selected_rows[0], 4]
    animal_name = df.iloc[selected_rows[0], 9]

    # Creating variables for latitude and longitude based off selected row
    latitude = df.iloc[selected_rows[0], 13]
    longitude = df.iloc[selected_rows[0], 14]

    # Return a leaflet Map object based on the selected row
    return [
        dl.Map(
            style={'width': '1000px', 'height': '500px'},
            center=[latitude, longitude],
            zoom=9,
            children=[

                # Using default TileLayer
                dl.TileLayer(),

                # Marker with tool tip and popup
                dl.Marker(
                    position=[latitude, longitude],
                    children=[

                        # Tooltip displays animal breed
                        dl.Tooltip(breed),

                        # Popup displays animal breed and animal name (if data available)
                        dl.Popup([
                            html.H3("Animal Breed"),
                            html.P(breed),
                            html.H3("Animal Name"),
                            html.P(animal_name),
                        ])
                    ]
                )
            ]
        )
    ]


if __name__ == '__main__':
    app.run_server(debug=True)