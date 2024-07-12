import ast
import matplotlib.pyplot as plt

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
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    # Plotting accuracy
    plt.subplot(2, 1, 2)
    plt.plot(epochs, [item['accuracy'][0] for item in data_list], label='Training Accuracy')
    plt.plot(epochs, [item['val_accuracy'][0] for item in data_list], label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Replace 'your_file_path.txt' with the actual path to your text file
file_path1 = 'history_file1.txt'
# Replace 'your_file_path.txt' with the actual path to your text file
file_path2 = 'history_file2.txt'

# Parse the data and plot
data_list = parse_data(file_path1)
plot_data(data_list)


# Parse the data and plot
data_list = parse_data(file_path2)
plot_data(data_list)
