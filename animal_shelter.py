from pymongo import MongoClient
import json

# --------------------------------------------------------------------
# A CRUD class developed in order to analyze data from animal shelters
# --------------------------------------------------------------------

class AnimalShelter(object):

    # init for connecting to mongodb with authentication
    def __init__(self, username, password):   
        
        # Calling the MongoClient function with username and password parameters
        self.client = MongoClient(
            'mongodb+srv://%s:%s@clientserver-app.kkumc2n.mongodb.net/?retryWrites=true&w=majority'%(username, password))

        # Accessing the AAC database through the client
        self.database = self.client['AAC']
    
    # The C in CRUD
    # Function to create a new document in the mongo database                              
    def create(self, data):
    
        # Checking to make sure the function call provided data
        if data is not None:
            
            # Insert the data into the animals collection in the database (AAC database)
            self.database.animals.insert(data)
            
            # Return True
            return True
        
        # If the function call provided no data
        else:
            
            # Print error message
            print("Error: No data")
            
            # Return False
            return False 
    
    # The R in CRUD - part 1
    # Function to read a single document from the mongo database                              
    def read(self, data):
        
        # Check to make sure the method call contained data
        if data is not None:

            # Calling the find_one function to retrieve a single matching document
            result = self.database.animals.find_one(data)
            
            # If the find_one method executed properly
            if result: 
                
                # return the result
                return result
            
            else:
                
                # Print failure message:
                print("Error: Read operation failed")
    
        # If method call contained no data...
        else:
            
            # Print error message
            print("Error: No data")
            return False
    
    # The R in CRUD - part 2
    # Function to read all matching documents from the mongo database                              
    def read_all(self, data):
        
        # Check to make sure the method call contained data
        if data is not None:
        
            # Calling the find function to retrieve a cursor for all matching documents
            # Using a projection to exclude the underscore id from the cursor
            result = self.database.animals.find(data, {'_id':False})
            
            # If the find method executed properly
            if result:
                
                # Return the result
                return result
               
            else:
                
                # Print failure message:
                print("Error: Read All operation failed")
                
        # If method call contained no data...
        else:
            
            # Print error message
            print("Error: No data")
            return False
    
    # The U in CRUD
    # Function to read all matching documents from the mongo database                              
    def update(self, data, operation):
        
        # Check to make sure the method call contained data
        if data is not None:

            # Calling the update_many function to update all matching documents
            result = self.database.animals.update_many(data, operation)
            
            # If the update_many method call executed properly...
            if result:                
                
                # Convert the raw_result to a JSON string and return it
                return json.dumps(result.raw_result)
            
            else:
                
                # Print failure message:
                print("Error: Update operation failed.")
    
        # If method call contained no data...
        else:
            
            # Print error message
            print("Error: No data")
            return False        
    
    # The D in CRUD
    # Function to read all matching documents from the mongo database                              
    def delete(self, data):
        
        # Check to make sure the method call contained data
        if data is not None:

            # Calling the delete_many function to delete all matching documents
            result = self.database.animals.delete_many(data)
            
            # If the delete_many method call executed properly...
            if result:                
                
                # Convert the raw_result to a JSON string and return it
                return json.dumps(result.raw_result)            
            
            else:
                
                # Print failure message:
                print("Error: Delete operation failed.")
    
        # If method call contained no data...
        else:
            
            # Print error message
            print("Error: No data")
            return False