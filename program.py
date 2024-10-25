import os
import cv2
import pandas as pd
import numpy as np
import odf

def calculate_thresholds(image):
    if len(image.shape) == 3:
        # Calculate average RGB values
        avg_color_per_row = np.mean(image, axis=0)
        avg_color = np.mean(avg_color_per_row, axis=0)

        # Calculate thresholds
        lower_threshold = avg_color - 20  # Lower threshold
        upper_threshold = avg_color + 20  # Upper threshold

        return lower_threshold, upper_threshold
    return None, None

# Path to the assets directory
assets_dir = 'assets'

# Prepare data storage
data = {
    'Image Name': [],
    'Red Lower': [], 'Red Upper': [],
    'Green Lower': [], 'Green Upper': [],
    'Blue Lower': [], 'Blue Upper': []
}

# Iterate over all files in the assets directory
for filename in os.listdir(assets_dir):
    if filename.endswith(('.png', '.jpg', '.jpeg')):  # Check for image file types
        # Construct full file path
        file_path = os.path.join(assets_dir, filename)

        # Load the image
        image = cv2.imread(file_path)
        if image is None:
            print(f"Error: Image not found at {file_path}")
            continue
        
        # Calculate thresholds
        lower_threshold, upper_threshold = calculate_thresholds(image)

        # Store results in data dictionary
        if lower_threshold is not None and upper_threshold is not None:
            data['Image Name'].append(filename)
            data['Red Lower'].append(lower_threshold[2])  # R channel
            data['Red Upper'].append(upper_threshold[2])  # R channel
            data['Green Lower'].append(lower_threshold[1])  # G channel
            data['Green Upper'].append(upper_threshold[1])  # G channel
            data['Blue Lower'].append(lower_threshold[0])  # B channel
            data['Blue Upper'].append(upper_threshold[0])  # B channel

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Save the DataFrame to an .ods file
df.to_excel('image_thresholds.ods', engine='odf')

print("Processing complete. Results saved to 'image_thresholds.ods'.")