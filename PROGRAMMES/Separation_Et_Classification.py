import pandas as pd
import os
from PIL import Image

csv_file = r"C:\Users\Pc\Desktop\testLabels15.csv"  # Replace with your CSV file path
image_dir = r"C:\Users\Pc\Desktop\test_2015"       # Replace with your image directory path
output_parent_dir = r"C:\Users\Pc\Desktop\test_classes_2015"  # Replace with your output parent directory path

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Desired image dimensions
new_size = (224, 224)

# Dictionary to keep track of the image count for each class
image_count_per_class = {}

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    image_name = row["image"]  # Replace with the actual column name for image in your CSV file
    class_label = row["level"]  # Replace with the actual column name for class level in your CSV file

    # Increment the image count for the current class
    if class_label in image_count_per_class:
        image_count_per_class[class_label] += 1
    else:
        image_count_per_class[class_label] = 1

    # Create the class output directory if it doesn't exist
    class_output_dir = os.path.join(output_parent_dir, str(class_label))
    os.makedirs(class_output_dir, exist_ok=True)

    # Build the new image name with the class label and image count
    new_image_name = f"{class_label}_test{image_count_per_class[class_label]:02d}.jpg"

    # Load and resize the image to the desired dimensions
    image_path, image_extension = os.path.splitext(os.path.join(image_dir, image_name))
    image_path += ".jpg"  # Add the ".jpg" extension here
    output_path = os.path.join(class_output_dir, new_image_name)

    # Print the image paths for debugging
    print(f"Image path: {image_path}")
    print(f"Output path: {output_path}")

    # Open the image
    img = Image.open(image_path)

    # Resize the image
    img_resized = img.resize(new_size, Image.LANCZOS)

    # Save the resized image as PNG
    img_resized.save(output_path, "PNG")

print("Toutes les images ont été redimensionnées et classées avec le nom modifié.")
