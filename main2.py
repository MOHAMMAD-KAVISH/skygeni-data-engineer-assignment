import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import sys

# Set up logging configuration to track events and errors
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

def load_data(file_path):
    """
    Load client data from a CSV file into a pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        logging.info("Data loaded successfully.")
        return df
    except Exception as e:
        logging.error(f"Failed to load data: {e}")
        sys.exit(1)  # Exit the program if the file can't be loaded

def clean_data(df):
    """
    Clean the DataFrame by removing rows with missing essential fields
    and converting data types as needed.
    """
    try:
        # Drop rows where 'Age' or 'Spending Score' is missing
        df = df.dropna(subset=['Age', 'Spending Score'])

        # Convert 'Age' to integer if not already
        df['Age'] = df['Age'].astype(int)

        logging.info("Data cleaned successfully.")
        return df
    except Exception as e:
        logging.error(f"Error during data cleaning: {e}")
        sys.exit(1)

def analyze_data(df):
    """
    Perform basic data analysis on the DataFrame:
    - Show basic statistics
    - Find average spending score by gender
    """
    try:
        print("\nDescriptive Statistics:")
        print(df.describe())

        print("\nAverage Spending Score by Gender:")
        print(df.groupby('Gender')['Spending Score'].mean())

        logging.info("Data analysis completed successfully.")
    except Exception as e:
        logging.error(f"Error during analysis: {e}")
        sys.exit(1)

def visualize_data(df):
    """
    Create visualizations to better understand client demographics and spending:
    - Age distribution
    - Spending score distribution by gender
    - Heatmap of correlation between numeric features
    """
    try:
        # Set seaborn style for better aesthetics
        sns.set(style="whitegrid")

        # Histogram of Age
        plt.figure(figsize=(8, 4))
        sns.histplot(df['Age'], bins=20, kde=True, color='skyblue')
        plt.title('Age Distribution of Clients')
        plt.xlabel('Age')
        plt.ylabel('Count')
        plt.show()

        # Boxplot of Spending Score by Gender
        plt.figure(figsize=(8, 4))
        sns.boxplot(x='Gender', y='Spending Score', data=df)
        plt.title('Spending Score Distribution by Gender')
        plt.show()

        # Correlation heatmap
        plt.figure(figsize=(8, 6))
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Heatmap')
        plt.show()

        logging.info("Visualizations generated successfully.")
    except Exception as e:
        logging.error(f"Visualization error: {e}")
        sys.exit(1)

def main():
    """
    Main function to execute the data processing workflow:
    1. Load the data
    2. Clean the data
    3. Analyze the data
    4. Visualize the data
    """
    file_path = 'client_data.csv'  # Path to the CSV file
    df = load_data(file_path)      # Step 1: Load
    df = clean_data(df)            # Step 2: Clean
    analyze_data(df)               # Step 3: Analyze
    visualize_data(df)             # Step 4: Visualize

# Entry point of the script
if __name__ == "__main__":
    main()
