import pickle

try:
    music = pickle.load(open("df.pkl", "rb"))
    print(music.head())  # Check the first few rows
except FileNotFoundError:
    print("Error: df.pkl not found!")
