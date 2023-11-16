"""
Recognize food: fruit, vegetable
"""

import os
from datetime import datetime
import cv2
from google.cloud import vision_v1p3beta1 as vision

# Setup google authen client key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client_key.json'

# Source path content all images
SOURCE_PATH = "C:/Users/Luigi T. Francisco/Documents/Fruit Counter and Estimation/Recognize-fruit/"

FOOD_TYPE = 'Fruit'  # 'Vegetable'


def load_food_name(food_type): # a function to load the dictionary
    """
    Load all known food type name.
    :param food_type: Fruit or Vegetable
    :return:
    """
    names = [line.rstrip('\n').lower() for line in open( food_type + '.dict')]
    return names

def localize_objects(path,list_food): # this is the function that counts the localize objects from google api
    # this also uses open cv2 to create bounding box from those objects 
    """Localize objects in the local image.
    
 
    Args:
    path: The path to the local file.
    """
    prices = { # price of the fruits
  "apple": 5,
  "pear": 20,
  "banana": 10,
  "peach" :30,
  "orange":25
   }
    object_price = 0
    total_price = 0
    start_time = datetime.now() # time the function started
    
    img = cv2.imread(path) # the original image being assigned to variable with opencv
    
    height, width = img.shape[:2] # dimensions of the image provided
    

    client = vision.ImageAnnotatorClient() # establishment of connection to the google vision

    with open(path, "rb") as image_file:
        content = image_file.read() # passing the image to the variable in another way for google vision
    image = vision.Image(content=content)
     # image is passed with function from google vision so it could be
    # passed to functions that google vision api provides

    objects = client.object_localization(image=image).localized_object_annotations
    #an array objects is created with contents given by the google vision api from the request to read the
    # variable vision image

    

    

    
   
    count = 0 # a variable for counting how many fruits are in the image
    for object_ in objects: # an iteration of objects in the array of objects
        print(f"\n{object_.name} (confidence:{object_.name})") # prints the possible term for the object
        print("Normalized bounding polygon vertices: ") # prints the bounding box google vision provided
        
        pointsx=[] # an array for storing corner x points of the object
        pointsy=[] # an array for storing corner y points of the object
        desc = object_.name.lower() # the label is turned to lowercase for comparison with the dictionary we have
        
    
       
        if (desc in list_foods): # compares the label of the object to the entries in the dictionary
            #if an object have the same name then a bounding box  is implemented and through the following loop
            object_price = prices.get(desc)
            total_price += object_price
            for vertex in object_.bounding_poly.normalized_vertices: # stores the given vertices by google api
                
                pointsx.append(vertex.x)
                pointsy.append(vertex.y)
        

            print(pointsx)
            print(pointsy)
            # start of reversing the normalization done by google vision api
            first_point_y = round(pointsy[0] * height)
            first_point_x = round(pointsx[0] * width)
            second_point_y  = round(pointsy[2] * height)
            second_point_x = round(pointsx[2] * width)
            # prints the actual coordinates for the upper left and lower right corner of the object
            print(first_point_x,first_point_y,second_point_x,second_point_y)
            count+=1 # adds one to the counter
            
            

        

            

                     
            
            #draws the rectangle by passing the image, coordinates, color of the rectangle , and thickness
            cv2.rectangle(img,(first_point_x,first_point_y),(second_point_x,second_point_y),(255,0,0),2)
            #draws a text of the probable fruit it was and the confidence level
            cv2.putText(img, desc.upper() + ","+str(round((object_.score),2))+" Price: "+ str(object_price), (first_point_x,first_point_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), )
    #draws the fruit counted by the end of array of objects.
    cv2.putText(img, 'Fruit Counted: '+str(count)+", Total Price: " + str(total_price),(10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), )
    #this is for terminal in the vs studio
    print(f"Number of fruits found: {count}")
    #total time it took for the fruits to be counted i guess
    print('Total time: {}'.format(datetime.now() - start_time))
    #writes to an output png the outcome     
    cv2.imwrite('output.png',img)
    alpha = cv2.imread("output.png")
    #opens a window with the output
    cv2.imshow('Recognize & Draw', alpha)
    
    cv2.waitKey(0)



print('---------- Start FOO D Recognition --------')
list_foods = load_food_name(FOOD_TYPE) # loads the dictionary to be used by the localize_objects function
localize_objects(('8.png'),list_foods) # calls the functipon that counts and estimates what fruit is there
print('---------- End ----------')
