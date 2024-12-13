import pandas as pd
import numpy as np

# Function to generate synthetic dataset
def generate_synthetic_data(size):
    np.random.seed(42)
    data = {
        'Age': np.random.randint(1, 100, size=size),
        'Sex': np.random.choice([0, 1], size=size),
        'BMI': np.random.uniform(15, 40, size=size),
        'Smoker': np.random.choice([0, 1], size=size),
        'HighBP': np.random.choice([0, 1], size=size),
        'HighChol': np.random.choice([0, 1], size=size),
        'Stroke': np.random.choice([0, 1], size=size),
        'HeartDiseaseorAttack': np.random.choice([0, 1], size=size),
        'PhysActivity': np.random.choice([0, 1], size=size),
        'HvyAlcoholConsump': np.random.choice([0, 1], size=size),
        'GenHlth': np.random.randint(1, 6, size=size),
        'MentHlth': np.random.randint(0, 30, size=size),
        'PhysHlth': np.random.randint(0, 30, size=size),
        'Diabetes_binary': np.random.choice([0, 1], size=size, p=[0.7, 0.3])  # 70% non-diabetic, 30% diabetic
    }
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Generate synthetic datasets
    print("Generating synthetic dataset with 1 million samples...")
    dataset_1m = generate_synthetic_data(1_000_000)
    dataset_1m.to_csv('synthetic_data_1m.csv', index=False)
    print("Dataset with 1 million samples saved as 'synthetic_data_1m.csv'.")

    print("\nGenerating synthetic dataset with 10 million samples...")
    dataset_10m = generate_synthetic_data(10_000_000)
    dataset_10m.to_csv('synthetic_data_10m.csv', index=False)
    print("Dataset with 10 million samples saved as 'synthetic_data_10m.csv'.")
