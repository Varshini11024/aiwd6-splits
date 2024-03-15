import os
import shutil

# Define paths
source_folder = '/home/varshini/Documents/Sem6/MP/aiwd6-splits/s_to_f/annotated_mask_s_to_f_final'
train_folder = '/home/varshini/Documents/Sem6/MP/aiwd6-splits/s_to_f/masks/train'
val_folder = '/home/varshini/Documents/Sem6/MP/aiwd6-splits/s_to_f/masks/val'
test_folder = '/home/varshini/Documents/Sem6/MP/aiwd6-splits/s_to_f/masks/test'

# Create destination folders if they don't exist
for folder in [train_folder, val_folder, test_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Initialize sets dictionary
sets_dict = {}

# Loop through the source folder
for filename in os.listdir(source_folder):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Extract set number from filename
        set_number = filename.split('_')[-2]

        # Append filename to the corresponding set
        if set_number not in sets_dict:
            sets_dict[set_number] = [filename]
        else:
            sets_dict[set_number].append(filename)

# Initialize counters
train_count = 0
val_count = 0
test_count = 0

# Distribute sets to train, val, and test folders
for set_number, images in sets_dict.items():
    # Decide destination folder for the entire set
    if train_count + len(images) <= 2080:
        dest_folder = train_folder
        train_count += len(images)
    elif val_count + len(images) <= 590:
        dest_folder = val_folder
        val_count += len(images)
    else:
        dest_folder = test_folder
        test_count += len(images)

    # Move all images of the set to the destination folder
    for image in images:
        source_path = os.path.join(source_folder, image)
        dest_path = os.path.join(dest_folder, image)
        shutil.move(source_path, dest_path)

print("Dataset divided successfully.")