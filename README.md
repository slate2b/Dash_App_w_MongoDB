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



