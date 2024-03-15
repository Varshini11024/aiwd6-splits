import os
import shutil
import json

# Define paths
source_folder = '/home/varshini/Documents/Sem6/MP/c_to_r/final_c_to_r'
train_folder = '/home/varshini/Documents/Sem6/MP/aiwd6-splits/c_to_r/images/train'
val_folder = '/home/varshini/Documents/Sem6/MP/aiwd6-splits/c_to_r/images/val'
test_folder = '/home/varshini/Documents/Sem6/MP/aiwd6-splits/c_to_r/images/test'

masks_folder = '/home/varshini/Documents/Sem6/MP/c_to_r/annotated_mask_c_to_r_final'

mask_train = '/home/varshini/Documents/Sem6/MP/aiwd6-splits/c_to_r/masks/train'
mask_test = '/home/varshini/Documents/Sem6/MP/aiwd6-splits/c_to_r/masks/test'
mask_val = '/home/varshini/Documents/Sem6/MP/aiwd6-splits/c_to_r/masks/val'

annotation_file = '/home/varshini/Documents/Sem6/MP/c_to_r/annotations_c_to_r.json'

annot_folder = '/home/varshini/Documents/Sem6/MP/aiwd6-splits/c_to_r/annotations'

with open(annotation_file, 'r') as f:
    annotations_data = json.load(f)


# Create destination folders if they don't exist
for folder in [train_folder, val_folder, test_folder, annot_folder, mask_val, mask_test, mask_train]:
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
 
train_annotation = {
    'info': annotations_data['info'], 
    'licenses': annotations_data['licenses'], 
    'categories': annotations_data['categories'], 
    'images': [], 
    'annotations': []
}

val_annotation = {
    'info': annotations_data['info'], 
    'licenses': annotations_data['licenses'], 
    'categories': annotations_data['categories'], 
    'images': [], 
    'annotations': []
}

test_annotation = {
    'info': annotations_data['info'], 
    'licenses': annotations_data['licenses'], 
    'categories': annotations_data['categories'], 
    'images': [], 
    'annotations': []
}


d = {'train': [], 'test': [], 'val': []}

# Distribute sets to train, val, and test folders
for set_number, images in sets_dict.items():
    # Decide destination folder for the entire set
    if train_count + len(images) <= 2080:
        dest_folder = train_folder
        dest_folder2 = mask_train
        train_count += len(images)
        d['train'].append(set_number)
    elif val_count + len(images) <= 590:
        dest_folder = val_folder
        dest_folder2 = mask_val
        val_count += len(images)
        d['val'].append(set_number)
    else:
        dest_folder = test_folder
        dest_folder2 = mask_test
        test_count += len(images)
        d['test'].append(set_number)

    # Move all images of the set to the destination folder
    for image in images:
        source_path = os.path.join(source_folder, image)
        mask_path = os.path.join(masks_folder, image)
        
        dest_path = os.path.join(dest_folder, image)
        mask_dest_path = os.path.join(dest_folder2, image)
        
        shutil.move(source_path, dest_path)
        shutil.move(mask_path, mask_dest_path)

for image in annotations_data['images']:
    # Update annotation file path for the moved image
    image_filename = image['file_name'].split('_')[-2]
    if image_filename in d['train']:
        # shutil.copy(os.path.join(images_folder, image_filename), os.path.join(train_folder, image_filename))
        # shutil.copy(os.path.join(masks_folder, image_filename), os.path.join(train_folder, image_filename.replace('.jpg', '_mask.jpg')))
        train_annotation['images'].append(image)
        train_annotation['annotations'].extend([annot for annot in annotations_data['annotations'] if annot['image_id'] == image['id']])
    elif image_filename in d['val']:
        # shutil.copy(os.path.join(images_folder, image_filename), os.path.join(val_folder, image_filename))
        # shutil.copy(os.path.join(masks_folder, image_filename), os.path.join(val_folder, image_filename.replace('.jpg', '_mask.jpg')))
        val_annotation['images'].append(image)
        val_annotation['annotations'].extend([annot for annot in annotations_data['annotations'] if annot['image_id'] == image['id']])
    elif image_filename in d['test']:
        # shutil.copy(os.path.join(images_folder, image_filename), os.path.join(test_folder, image_filename))
        # shutil.copy(os.path.join(masks_folder, image_filename), os.path.join(test_folder, image_filename.replace('.jpg', '_mask.jpg')))
        test_annotation['images'].append(image)
        test_annotation['annotations'].extend([annot for annot in annotations_data['annotations'] if annot['image_id'] == image['id']])


class NewlineSeparator(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super(NewlineSeparator, self).__init__(*args, **kwargs)

    def encode(self, o):
        result = super(NewlineSeparator, self).encode(o)
        return result.replace(',', ',\n')


# Save updated annotations to new JSON files with new lines after commas
with open(os.path.join(annot_folder, 'train.json'), 'w') as f:
    json.dump(train_annotation, f, cls=NewlineSeparator)
    f.write('\n')

with open(os.path.join(annot_folder, 'val.json'), 'w') as f:
    json.dump(val_annotation, f, cls=NewlineSeparator)
    f.write('\n')

with open(os.path.join(annot_folder, 'test.json'), 'w') as f:
    json.dump(test_annotation, f, cls=NewlineSeparator)
    f.write('\n')



print("Dataset divided successfully and annotations splitted.")
