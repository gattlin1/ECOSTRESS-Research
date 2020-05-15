# NASA MOSGC Ecostress Research

------

This project contains the work for the spectral similarity algorithms and the
convolutional neural network.

## Spectra Comparison

### Hardware Requirements

The only real requirement is a computer that has at least 8 cores. The hitlist utilizes 8 cores to run the 4 algorithms with and without NLC. A computer without this amount of cores can still run them but runtimes will be increased.

### Library Requirements

The only external library found is one called "Colorama". It is a library that adds color to the terminal output. It is by no means necessary but it is easier for the user to scan through data since things are certain colors. This can be installed with **pip install colorama**.

### Workflow

hitlist.py is the class that handles all of the hitlist operations. run_hitlist.py is the script that runs the hitlist for all of the algorithms. The results are stored in the same directory with a timestamp as the folder for each run. Each algorithm's results are stored in a file in this directory.

## CNN

### Hardware Requirements

This isn't really a requirement but a good GPU would be preferred for this area. Most of the computers in the lab have ones that are good enough. It is by no means required but it is definitely going to speed up the training and testing process

### Library Requirements

 The main area is Tensorflow GPU. My computer already has the GPU setup but it can be run just the regular version of Tensorflow. I would not recommend it, however. The runtime for training these models will be incredibly long without the GPU version. If you are needing to get the GPU setup on a new computer, I would recommend watching a youtube video or looking up a tutorial on google over the subject. There is a lot of great documentation over the subject and the guides walk you through every step of the way. Keras is the API used for the models. **Numpy, Matplotlib, Pandas, and OpenCV** are the other libraries used. These can also be installed with pip.

### Workflow

Each directory is sectioned off for each type of model.  New Categories is doing the same thing but for the classes Dr. Yoshimatsu suggested. Spectrum Similarity is using the CNN approach with the hitlist. Inside each directory is a data folder with file to create the pickles used for the model.