# Dash App with MongoDB

This project is a Client-Server Dashboard Application which follows the Model View Controller (MVC) Software Design Pattern.  It uses the RESTful protocol for additional utility and security.  The application includes a database and a client-facing web application dashboard which allows users to interact with the data through filter options and a data table.  The dashboard also provides data visualization through a pie chart and a geolocation chart which update based on the user’s interactions with the filters and the data table.  I originally created the sketch of this application in my Client-Server Application Development class at Southern New Hampshire University, but this version includes several changes.

The application was designed for a hypothetical client named Grazioso Salvare,
a company which trains rescue animals.  The client needed to be able to quickly analyze data from local animal shelters to identify potential candidates for rescue training.

The original project used a conventional MongoDB database as the data model with the view and controller components implemented in Jupyter Notebook.  For this implementation, however, I switched to MongoDB Atlas for the data model and switched to all Python source code for the view and controller (not Jupyter).

This project includes the following modules, libraries, components, widgets, etc:

  - CRUD module (animal_shelter.py) which handles the interactions between the dashboard and the data model
  - The source code for the dashboard (dashboard.py)
  - MongoDB Atlas database
  - Dash Framework
  - Pandas DataFrame
  - Dash DataTable
  - Dash-Leaflet Geolocation Chart
  - Plotly Express Pie Chart

The CRUD module and dashboard could be easily adapted for use in any number of client-server applications.

# Screenshot of Dashboard on Initial Load

![ClientServerApp_screenshot1](https://user-images.githubusercontent.com/88697660/198503069-71e44f21-204f-46e9-b199-597c6b3894fb.PNG)

# Getting Started

To get a local copy of this application up and running, there are some initial steps which must be followed, including downloading project files and preparing the MongoDB.  Please review the following steps to get started:

Create a new project in your Python IDE.
Download the following project files and copy/paste them into your python project folder.

- animal_shelter.py
- dashboard.py
- aac_shelter_outcomes.csv
- Grazioso Salvare Logo.png

To use the application with the same database names, collection names, and data as the current test implementation uses, follow these steps:

- Import the aac_shelter_outcomes.csv file into MongoDB as a new database called ‘AAC’ with a collection name of ‘animals’.  Please note: the csv file does contain headers.  
- Create a user in the AAC database with read-write privileges called ‘gsUser’ and a password of ‘gsUserPass1’.  
- Please note: In this current implementation, the username and password are passed to the animal_shelter.py module via the test script itself.  
- Feel free to change the username and password, just be sure to change them in the dashboard.py file as well.  
- Make sure MongoDB is up and running (if using Atlas, not a concern)
- Update the MongoClient connection string in the animal_shelter.py file to match your socket or Atlas string.  
- This should properly configure the Mongo database to work with the CRUD module and the dashboard application.  

The animal_shelter.py CRUD module includes Create, Read, Read_All, Update, and Delete functionality, and the dashboard.py file contains the source code for the client-facing dashboard.  

# Installation

Although this application has been designed to meet a particular business need, its functionality can be applied to many different scenarios.  It can likewise be tested and / or implemented with a few tweaks with any existing MondoDB database.  

The tools required for running this project include:

- MongoDB
- Any Python IDE

For help installing and configuring MongoDB, this is a good place to start:
https://www.mongodb.com/

As far as Python libraries go, this project makes use of the following:

- pymongo
- json
- dash
- dash-leaflet
- plotly express
- base64
- Pandas

Once all tools and libraries have been installed and the MongoDB database has been set up (see the Getting Started section above), you should be ready to run the application.

The dashboard.py file is the driver class for this application, so simply run the dashboard.py file in your IDE in order to run the application.

# Usage

As previously mentioned, this application includes a python module for the AnimalShelter class which provides full CRUD functionality.  It uses the PyMongo driver to access data in MongoDB. The application also includes a dashboard.py file which contains the source code for the dashboard and various interactions between the CRUD module and the MongoDB database itself.  

Once the application is up and running, using the dashboard is intuitive.

There are four radio buttons which allow a user to filter the results of the data table and subsequently the pie chart and geolocation chart based on the criteria provided by the hypothetical business.  The business identified particular criteria for rescue animals which suit common needs, including water rescue, mountain rescue and disaster rescue.  Selecting one of the radio buttons accesses the Mongo database and returns data for animals which meet those particular business needs.  

The pie chart displays a percentage breakdown of the results of the data frame according to breed.  The pie chart updates based on the filter selected by the user.  

The geolocation chart displays a marker for the selected animal.  It defaults to the first record in the data table results, but if the user selects the row in the data table for an individual animal, the marker will update to the location of the selected animal.  Hovering over the marker will display a tool tip showing the animal’s breed.  Clicking on the marker displays a pop-up with the animal’s breed and the animal’s name.

Using the filter radio buttons allows a user to quickly review the animals which meet the criteria as defined by the business.  

The pie chart provides insights into the breeds of animals which match the filter criteria.  

The geolocation chart provides insights into the proximity of the animals which match the filter criteria to the area of business need.

Clicking the reset filter radio button clears all filters and returns all records to the data table.  

And lastly, just for kicks, clicking the company’s logo routes the user to my github profile.  

# Code Examples

"""
CRUD class in the animal_shelter.py CRUD module
"""
class AnimalShelter(object):

    #init for connecting to mongodb with authentication
    def __init__(self, username, password):   
        
        #Calling the MongoClient function with username and password parameters
        self.client = MongoClient(
            'mongodb+srv://%s:%s@clientserverxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'%(username, password))

        #Accessing the AAC database through the client
        self.database = self.client['AAC']

"""
Function in the animal_shelter.py CRUD Module to read all matching documents from the mongo database                              
""" 
def read_all(self, data):
        
    #Check to make sure the method call contained data
    if data is not None:

        #Calling the find function to retrieve a cursor for all matching documents
        #Using a projection to exclude the underscore id from the cursor
        result = self.database.animals.find(data, {'_id':False})

        #If the find method executed properly
        if result:

            #Return the result
            return result

        else:

            #Print failure message:
            print("Error: Read All operation failed")

    #If method call contained no data...
    else:

        #Print error message
        print("Error: No data")
        return False
        
"""
Creating a CRUD object and accessing the Data Model (MongoDB) in the dashboard.py file
"""
#Hard-coding the username and password into the current implementation
username = "gsUser"
password = "gsUserPass1"

#Creating a AnimalShelter (CRUD class) object
shelter = AnimalShelter(username, password)

#Calling the read_all method from the CRUD module and creating a pandas DataFrame
df = pd.DataFrame.from_records(shelter.read_all({}))

"""
Radio Items for the View component used in filter callback tied to the data table in the dashboard.py file
"""
#RadioItems to filter results in the data table and charts
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

"""
Callback in the dashboard.py file returns data frame data and columns based on radio item selections from the user and returns the selected row to the top row displayed in the data table
"""
@app.callback([Output('datatable-id', 'data'),
               Output('datatable-id', 'columns'),
               Output('datatable-id', 'selected_rows')],
              [Input('radio-items-id', 'value')])
def update_dashboard(filter_type):

    #Default will include all records
    df = pd.DataFrame(list(shelter.read_all({})))

    #If user clicks Water Rescue
    if (filter_type == 1):
        df = pd.DataFrame(list(shelter.read_all({
            "animal_type": "Dog",
            "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": {"$gte": 26},
            "age_upon_outcome_in_weeks": {"$lte": 156}})))

    #If user clicks Mountain Rescue
    elif (filter_type == 2):
        df = pd.DataFrame(list(shelter.read_all({
            "animal_type": "Dog",
            "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog",
                              "Siberian Husky", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26},
            "age_upon_outcome_in_weeks": {"$lte": 156}})))

    #If user clicks Distaster Rescue
    elif (filter_type == 3):
        df = pd.DataFrame(list(shelter.read_all({
            "animal_type": "Dog",
            # NOTE: Using breed name 'Doberman Pinsch' to match breed name in data set
            "breed": {"$in": ["Doberman Pinsch", "German Shepherd", "Golden Retriever",
                              "Bloodhound", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 20},
            "age_upon_outcome_in_weeks": {"$lte": 300}})))

    #If user clicks reset
    elif (filter_type == 4):
        df = pd.DataFrame(list(shelter.read_all({})))

    #Set columns to return
    columns = [{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]

    #Set data to return based on conditional logic above
    data = df.to_dict('records')

    #Reset the selected row to the first row
    row = [0]

    #Return the data and columns based on user's filter radio item selection
    return (data, columns, row)

"""
Callback in the dashboard.py file returns an updated geolocation chart based on selections and filters in the datatable
"""

@app.callback(
    Output('map-id', 'children'),
    [Input('datatable-id', 'data'), Input('datatable-id', 'selected_rows')]
)
def update_map(viewData, selectedRows):

    #Dataframe used for the Geolocation Chart based on datatable input
    df = pd.DataFrame.from_dict(viewData)

    #List of row positions for all selected rows. Current implementation only allows single row.
    selected_rows = selectedRows

    #If no rows currently selected, geolocation defaults to the data from the top row of the dataframe
    #NOTE: If filtered, the geolocation chart will update based on the top row of the filtered dataframe
    if not selectedRows:
        selected_rows = [0]

    #Creating variables for data to be displayed in the marker's tooltip and popup based off selected row
    breed = df.iloc[selected_rows[0], 4]
    animal_name = df.iloc[selected_rows[0], 9]

    #Creating variables for latitude and longitude based off selected row
    latitude = df.iloc[selected_rows[0], 13]
    longitude = df.iloc[selected_rows[0], 14]

    #Return a leaflet Map object based on the selected row
    return [
        dl.Map(
            style={'width': '1000px', 'height': '500px'},
            center=[latitude, longitude],
            zoom=9,
            children=[

                #Using default TileLayer
                dl.TileLayer(),

                #Marker with tool tip and popup
                dl.Marker(
                    position=[latitude, longitude],
                    children=[

                        #Tooltip displays animal breed
                        dl.Tooltip(breed),

                        #Popup displays animal breed and animal name (if data available)
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

# Screenshot of Data Table with radio button filter active and animal selected

![ClientServerApp_screenshot5](https://user-images.githubusercontent.com/88697660/198503426-914e228b-8f1d-4641-9386-326787032bb7.PNG)

# Screenshot of Geolocation Chart fed by selected animal in data table

![ClientServerApp_screenshot6](https://user-images.githubusercontent.com/88697660/198503454-80529669-25d3-4909-b263-9e9b71caf6e4.PNG)

# Screenshot of Pie Chart fed by active data table filter

![ClientServerApp_screenshot7](https://user-images.githubusercontent.com/88697660/198503465-e04b8088-a559-470b-9ee3-00fb097a303c.PNG)
