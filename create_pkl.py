import pickle
import pandas as pd

# Sample data to save in the .pkl file
data = pd.DataFrame({
    "song": ["Cold As You", "Long Live", "Superstar", "love"],
    "artist": ["Taylor Swift", "Bosson", "Barbie", 'ari']
})

# Specify the file path (it will be created in the project directory)
file_path = "df.pkl"

# Open the file in write-binary mode and save the data
with open(file_path, "wb") as file:
    pickle.dump(data, file)

    

print(f"Pickle file '{file_path}' created successfully!")
