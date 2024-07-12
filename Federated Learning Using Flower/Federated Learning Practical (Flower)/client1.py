import flwr as fl
import tensorflow as tf
from tensorflow import keras
import sys
import seaborn as sns
import ast
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# AUxillary methods
def getDist(y):
    # Use Counter to count occurrences of each digit
    counts = Counter(y)

    # Extract digits and counts for plotting
    digits, digit_counts = zip(*sorted(counts.items()))

    # Create a bar graph
    plt.bar(digits, digit_counts, color='skyblue')
    plt.xlabel('Digit')
    plt.ylabel('Count')
    plt.title('Client 1: Count of Each Digit in the List')
    plt.show()

def getData(dist, x, y):
    dx = []
    dy = []
    counts = [0 for i in range(10)]
    for i in range(len(x)):
        if counts[y[i]]<dist[y[i]]:
            dx.append(x[i])
            dy.append(y[i])
            counts[y[i]] += 1
        
    return np.array(dx), np.array(dy)

# Function to parse the data from the text file
def parse_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        data_list = [ast.literal_eval(line) for line in lines]
    return data_list

# Function to plot the data
def plot_data(data_list):
    epochs = range(1, len(data_list) + 1)

    # Plotting loss
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(epochs, [item['loss'][0] for item in data_list], label='Training Loss')
    plt.plot(epochs, [item['val_loss'][0] for item in data_list], label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Rounds')
    plt.ylabel('Loss')
    plt.legend()

    # Plotting accuracy
    plt.subplot(2, 1, 2)
    plt.plot(epochs, [item['accuracy'][0] for item in data_list], label='Training Accuracy')
    plt.plot(epochs, [item['val_accuracy'][0] for item in data_list], label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Rounds')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Replace 'your_file_path.txt' with the actual path to your text file
file_path1 = 'history_file1.txt'

# Load and compile Keras model
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])
model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
# model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])


# Load dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data(path='mnist.npz')
x_train, x_test = x_train[..., np.newaxis]/255.0, x_test[..., np.newaxis]/255.0
dist = [4000, 4000, 4000, 3000, 10, 10, 10, 10, 4000, 10]
x_train, y_train = getData(dist, x_train, y_train)
getDist(y_train)

# Define Flower client
class FlowerClient(fl.client.NumPyClient):
    # Download current state of the model
    def get_parameters(self, config):
        return model.get_weights()

    # Take the download weights and train the model on the top of it
    def fit(self, parameters, config):
        model.set_weights(parameters)
        r = model.fit(x_train, y_train, epochs=1, validation_data=(x_test, y_test), verbose=0)
        hist = r.history
        # Save the history to the text file
        with open(file_path1, 'a') as file:
            file.write(str(hist) + '\n')
        # Parse the data and plot
        data_list = parse_data(file_path1)
        plot_data(data_list)
        print("Fit history : ", hist)
        return model.get_weights(), len(x_train), {}


    # Test the modal
    def evaluate(self, parameters, config):
        model.set_weights(parameters)
        loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
        print("Eval accuracy : ", accuracy)
        return loss, len(x_test), {"accuracy": accuracy}


# Start Flower client
fl.client.start_numpy_client(
        server_address="localhost:5002", 
        client=FlowerClient(), 
        grpc_max_message_length = 1024*1024*1024
)
