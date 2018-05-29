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

Inference is currently being run on an image from [Landsat8](https://www.usgs.gov/products/data-and-tools/real-time-data/remote-land-sensing-and-landsat).
## Model Choice

A [ResNet architecture](https://arxiv.org/abs/1512.03385) was chosen for the CNN due to it's
fast inference time, good accuracy and smaller model size. See this [paper](https://arxiv.org/pdf/1605.07678.pdf)
for a comparison on all of these traits for the most common CNN architectures.

## Limitations

The current model has multiple limitations:

1. The model was trained on only images of the Amazon rainforest, but inference is being done on an image of California
    - This was done to get the full prototype working quickly
2. Inference is currently being run on a Landsat image (cut into tiles), while the model was trained using Planet satellite imagery
    - This was done due to Landsat imagery being more accessible than Planet imagery, and as an experiment
    to see how well the model performs on different target data
    - It is surprising it works somewhat well with this major difference im test data!
3. The current repo on GitHub is missing the Resnet50 weights due to GitHub file size restrictions
