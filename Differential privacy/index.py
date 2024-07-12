import numpy as np

def laplace_mechanism(query_result, sensitivity, epsilon):
    """
    Add Laplace noise to the query result to achieve differential privacy.
    
    Parameters:
        query_result (float): The true result of the query on the database.
        sensitivity (float): The sensitivity of the query, i.e., the maximum amount the query result can change by adding or removing one entry from the database.
        epsilon (float): The privacy parameter controlling the amount of noise to add. Smaller values provide more privacy but may reduce utility.
    
    Returns:
        float: The perturbed result after adding Laplace noise.
    """
    scale = sensitivity / epsilon
    noise = np.random.laplace(loc=0, scale=scale)
    return query_result + noise

# Example usage
true_result = 100  # Example: Total count of a certain attribute in a database
sensitivity = 1    # Example: Adding or removing one entry can change the count by at most 1
epsilon = 0.7      # Example: Privacy parameter, lower values provide more privacy
print("True result:", true_result)

for _ in range(10):
    perturbed_result = laplace_mechanism(true_result, sensitivity, epsilon)
    print("Perturbed result:", perturbed_result)