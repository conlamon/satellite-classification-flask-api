'''
Helper file to implement functions for directly dealing with the tensorflow model
'''
import numpy as np
from PIL import Image
import tensorflow as tf
from keras.applications.resnet50 import preprocess_input
from keras.models import model_from_json
from keras.preprocessing.image import img_to_array
import os
import gc



def load_model():
    '''
    Load the classification model from stored weights
    Updates global variables

    Note: Make sure this is run prior to starting the API to prevent request errors

    '''
    global model, classes, graph

    # Load in the model and weights
    with open('project/static/tfmodel/resnet50_model.json', 'r') as raw_json:
        loaded_json_model = raw_json.read()
        model = model_from_json(loaded_json_model)
    model.load_weights('project/static/tfmodel/resnet50_weights.hdf5')

    # Load in the classes
    with open('project/static/tfmodel/classes.txt', 'r') as class_file:
        for line in class_file:
            classes = line.split(" ")
    classes = np.array(classes).reshape(1, len(classes))

    # Define the global TensorFlow graph
    graph = tf.get_default_graph()

    print("Successfully loaded the model!")


def _load_image(image_path, target=(256, 256)):
    '''
    Private helper function to convert the image to a numpy array and do pre-processing

    Input:  image_path -- string; The path the the image, locally, in DB or on cloud service
            target -- tuple of ints; The target size of the image, height x width

    Output: image -- numpy array; Image converted to numpy array of shape (1xHxWx3)
    '''
    # Read in the image
    image = Image.open(image_path)

    # if the image mode is not RGB, convert it
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Check if we need to resize the input image
    width, height = image.size
    target_width, target_height = target
    if width != target_width or height != target_height:
        image = image.resize(target)

    # Convert the image to a numpy array
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)

    # Return the processed image
    return image


def predict(image_path):
    '''
    Prediction function that calls the classification model and returns predictions

    Input: image_path -- string; the path to the image returned form the database

    Output: data -- dict; JSON format containing the top prediction classes and probabilities
    '''
    data = {"success": False}

    # Load the image
    image = _load_image(image_path, target=(256, 256))

    # Use the default TensorFlow graph to ensure previously loaded model/weights are used
    with graph.as_default():
        # Make a prediction
        predictions = model.predict(image)

        # Free up image resources
        del image
        gc.collect()

        # Set a mask and filter predictions
        prediction_cutoff = os.environ.get('PREDICTION_CUTOFF', '0.1')
        pred_mask = predictions > float(prediction_cutoff)

        predicted_probabilities = predictions[pred_mask]

        predicted_classes = classes[pred_mask]

        # Update dictionary to return as response
        data["predictions"] = []
        for label, prob in zip(predicted_classes, predicted_probabilities):
            r = {"label": label, "probability": float(prob)}
            data["predictions"].append(r)

        # indicate that the request was a success
        data["success"] = True

        # return the data dictionary as a JSON response
        return data
