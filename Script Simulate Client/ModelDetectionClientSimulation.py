import re

def detect_model_poisoning(code):
    # Regex patterns to identify the model weight paths and aggregation
    model_weights_pattern = re.compile(r"model_client(\d+)_weights")
    aggregation_pattern = re.compile(r"aggregated_weights\s*=\s*{.?\((.?)\['coefficients'\]\s*\+\s*(.?)\['coefficients'\]\).?\}", re.DOTALL)

    # Extract all clients mentioned in the code
    clients = set(model_weights_pattern.findall(code))

    # Find all aggregation parts of the code
    aggregation_matches = aggregation_pattern.findall(code)

    if not aggregation_matches:
        return "No valid aggregation found in the code."

    results = []

    for match in aggregation_matches:
        first_client, second_client = match

        # Extract client numbers used in aggregation
        first_client_num = re.search(r"model_client(\d+)_weights", first_client).group(1)
        second_client_num = re.search(r"model_client(\d+)_weights", second_client).group(1)

        # Check if both clients are used in the aggregation
        if first_client_num != second_client_num and first_client_num in clients and second_client_num in clients:
            results.append("Safe aggregation: Both clients are used in aggregation.")
        else:
            results.append("Model poisoning detected: One client is left out in aggregation (Biased Model)")

    return results

# Normal code example
normal_code = '''
# Load the saved model weights for client 1 and client 2

model1_weights_path = '/content/model_client1_weights.pkl'
model2_weights_path = '/content/model_client2_weights.pkl'

model_client1_weights = joblib.load(model1_weights_path)
model_client2_weights = joblib.load(model2_weights_path)

# Aggregate model weights
aggregated_weights = {
    'coefficients': (model_client1_weights['coefficients'] + model_client2_weights['coefficients']) / 2,
    'intercept': (model_client1_weights['intercept'] + model_client2_weights['intercept']) / 2
}

# Save the aggregated model weights
aggregated_weights_path = '/content/aggregated_model_weights.pkl'
joblib.dump(aggregated_weights, aggregated_weights_path)
'''

# Poison code example
poison_code = '''
# Load the saved model weights for client 1 and client 2

model1_weights_path = '/content/model_client1_weights.pkl'
model2_weights_path = '/content/model_client2_weights.pkl'

model_client1_weights = joblib.load(model1_weights_path)
model_client2_weights = joblib.load(model2_weights_path)

# Aggregate model weights
aggregated_weights = {
    'coefficients': (model_client1_weights['coefficients'] + model_client1_weights['coefficients']) / 2,
    'intercept': (model_client1_weights['intercept'] + model_client1_weights['intercept']) / 2
}

# Save the aggregated model weights
aggregated_weights_path = '/content/aggregated_model_weights_poisoned.pkl'
joblib.dump(aggregated_weights, aggregated_weights_path)
'''

# Detect model poisoning in the normal code
normal_results = detect_model_poisoning(normal_code)
for result in normal_results:
    print(result)

# Detect model poisoning in the poison code
poison_results = detect_model_poisoning(poison_code)
for result in poison_results:
    print(result)