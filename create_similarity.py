import pickle
import numpy as np

# Example: Generate a dummy similarity matrix (replace with actual logic)
similarity_matrix = np.random.rand(10, 10)

# Save it as a pickle file
with open('similarity.pkl', 'wb') as f:
    pickle.dump(similarity_matrix, f)
