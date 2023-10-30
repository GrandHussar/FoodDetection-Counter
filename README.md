# Fruit Detection and Counter
Recognize fruit with Python, openCV and Google vision AI


### Requirements:
- Python 3
- GCP account (To use google vision)
- OpenCV (To scale image only)

### pip installations
pip install --upgrade google-cloud-vision

pip install --upgrade opencv-python


Credits to that guy from https://github.com/nimadorostkar/Recognize-fruit
i just improved upon this

In order to make it work i changed the label finder of google vision to localized objects for multiple objects to be detected and counted.

There it was able to count the objects

Now i compared those objects to my list of fruit 

If its in the list of fruit then i box that object using the normalized vertices received from google vision API 

The normalized vertcies are set inside a list for point X and Y respectively and then multiplied by Height(y) or Width(x).

The i call upon the cv2.rectangle with those coordinates.

Then i put a text on what was the label compared to and the confidence given corresponding to the label.




