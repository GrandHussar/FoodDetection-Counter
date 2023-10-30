"""
Recognize food: fruit, vegetable
"""

import io
import os
from datetime import datetime
import numpy

import cv2
from google.cloud import vision_v1p3beta1 as vision

# Setup google authen client key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client_key.json'

# Source path content all images
SOURCE_PATH = "C:/Users/Luigi T. Francisco/Documents/Fruit Counter and Estimation/Recognize-fruit/"

FOOD_TYPE = 'Fruit'  # 'Vegetable'


def load_food_name(food_type):
    """
    Load all known food type name.
    :param food_type: Fruit or Vegetable
    :return:
    """
    names = [line.rstrip('\n').lower() for line in open( food_type + '.dict')]
    return names

def localize_objects(path,list_food):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    img = cv2.imread(path)
    height, width = img.shape[:2]
    

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(image=image).localized_object_annotations
    

    
    (number_of_rows, number_of_columns) = img.shape[:2]
    count = 0
    for object_ in objects:
        print(f"\n{object_.name} (confidence:{object_.name})")
        print("Normalized bounding polygon vertices: ")
        pointsx=[]
        pointsy=[]
        desc = object_.name.lower()
    
       
        if (desc in list_foods):
            for vertex in object_.bounding_poly.normalized_vertices:
                
                pointsx.append(vertex.x)
                pointsy.append(vertex.y)

            print(pointsx)
            print(pointsy)
            
            first_point_y = round(pointsy[0] * height)
            first_point_x = round(pointsx[0] * width)
            second_point_y  = round(pointsy[2] * height)
            second_point_x = round(pointsx[2] * width)
            print(first_point_x,first_point_y,second_point_x,second_point_y)
            count+=1

        

            

                     
            
            
            cv2.rectangle(img,(first_point_x,first_point_y),(second_point_x,second_point_y),(255,0,0),2)
            cv2.putText(img, desc.upper() + ","+str(round((object_.score),2)), (first_point_x,first_point_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), )
    cv2.putText(img, 'Fruit Counted: '+str(count),(10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), )
    print(f"Number of fruits found: {count}")
    cv2.imshow('Recognize & Draw', img) 
    cv2.waitKey(0)



print('---------- Start FOOD Recognition --------')
list_foods = load_food_name(FOOD_TYPE)
localize_objects(('6.png'),list_foods)

print('---------- End ----------')
