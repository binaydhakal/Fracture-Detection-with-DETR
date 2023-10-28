import os
import pandas as pd
import json

import Annotations.coco_format as fracture_annotations


train_csv_path = 'fracture_split/train.csv'
test_csv_path = 'fracture_split/test.csv'
valid_csv_path = 'fracture_split/valid.csv'

train_df = pd.read_csv(train_csv_path)
test_df = pd.read_csv(test_csv_path)
valid_df = pd.read_csv(valid_csv_path)

annotations_file_path = 'Annotations/coco_format/fracture.json'

with open(annotations_file_path, 'r') as json_file:
    annotation_json_data = json.load(json_file)

def create_annotation_file(df, type):
    annotation_format = {
        "info": { "description": "Fracture Detection" },
        "categories": [{ "id": 0, "name": "fractured" }],
        "images": [],
        "annotations": []
    }
    for image in df['image_id']:
        image_data = [ann_image for ann_image in annotation_json_data["images"] if ann_image['file_name'] == image][0]
        annotation_data = [ann_image for ann_image in annotation_json_data["annotations"] if ann_image['image_id'] == image_data["id"]][0]
        annotation_format["images"].append(image_data)
        annotation_format["annotations"].append(annotation_data)
        with open(f'{type}.json', 'w') as file:
            file.write(json.dumps(annotation_format, indent=3))

create_annotation_file(train_df, 'train')
create_annotation_file(test_df, 'test')
create_annotation_file(valid_df, 'valid')
