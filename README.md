# Earth Classification API

## Basic Overview

A Python and Flask based REST API that serves a Keras/TensorFlow Convolutional Neural Network (CNN) model
trained to classify satellite image tiles into 17 different possible labels.
This API currently interfaces with a [React and Leaflet front-end](https://github.com/conlamon/varianceEarth).


![Site](https://github.com/conlamon/varianceEarth/blob/master/media/variancearth.png)


## How It Works

When the user clicks on an area selected on the map, a POST request, containing the center latitude/longitude coordinate
for the area selected, is sent to the REST API. The API then searches a PostgreSQL database for the file location of a satellite image tile
containing the selected area. This image is then processed, in real time, through a Keras/TensorFlow ResNet50
model. This model makes a multilabel classification over 17 different labels returning a score between 0 and 1 for each label.
The resultant scores are filtered based on a cutoff value, and then returned as JSON to the front-end.

## Data

The model was trained using the public [dataset](https://www.kaggle.com/c/planet-understanding-the-amazon-from-space/data)
from [Planet](https://api.planet.com.) that was part of their Kaggle competition in 2017.
This dataset consisted of ~42,000 image tiles of the amazon rainforest, all labeled.
The main labels that appear in the current implementation are defined as the following:

| Label       | Description
| :-------------: |-------------|
| No Clouds    | No clouds in the image |
| Primary      | A segment of dense tree cover |
| Habitation | Any human homes or buildings |
| Agriculture | Any area of agriculture |
| Road | Any road within the image |
| Water | River or Lake |

There are many more labels which can be found [here](https://www.kaggle.com/c/planet-understanding-the-amazon-from-space/data).

## Model Choice

A [ResNet architecture](https://arxiv.org/abs/1512.03385) was chosen for the CNN due to it's
fast inference time, good accuracy and smaller model size. See this [paper](https://arxiv.org/pdf/1605.07678.pdf)
for a comparison on all of these traits for the most common CNN architectures.

## Notes on Design and Possible Improvements

The following are some design choices and possible improvements:

1. The model was trained on only images of the Amazon rainforest, but inference is being done on an image of California
    - This was done to get the full prototype working quickly
2. The area selected by the user is not always the entire area that gets classified:
    - The center lat/lng coordinate of the image is used to find the image tile that encompasses that area, and this
    is the image that is classified
    - As a result, some selections on the map (particularly smaller selections) make less sense
    - This design choice can be improved in future iterations by improving the area selection algorithm and batch processing multiple images if needed, then aggregating the final predictions
