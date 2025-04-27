import os
import shutil
import random
from pathlib import Path
from google.colab import files



## kaggle_downloader.py
## Download Kaggle dataset or competition files

# Function to setup Kaggle API
def setup_kaggle():
    """
    Installs and configures Kaggle API by uploading and placing kaggle.json.
    """
    print("Please upload your 'kaggle.json' file:")
    uploaded = files.upload()

    if 'kaggle.json' not in uploaded:
        raise FileNotFoundError("Upload failed. Please download 'kaggle.json' from your Kaggle account settings.")

    # Create .kaggle directory and move the file
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_dir.mkdir(parents=True, exist_ok=True)
    shutil.move("kaggle.json", kaggle_dir / "kaggle.json")
    os.chmod(kaggle_dir / "kaggle.json", 0o600)

    print("✅ Kaggle API is configured successfully!")

# Function to download Kaggle dataset or competition files
def download_kaggle_data(dataset_path, setup_kaggle_api=True, is_competition=False, unzip=True, delete_zip=True):
    """
    Downloads and extracts a dataset or competition files from Kaggle.

    Args:
        dataset_path (str): Dataset in the format 'username/dataset-name' or just 'competition-name'
        setup_kaggle_api (bool): Set to True to configure Kaggle API before downloading
        is_competition (bool): Set to True if downloading competition files
        unzip (bool): Set to True to unzip the downloaded file
        delete_zip (bool): Set to True to delete the .zip file after extraction
    """
    if setup_kaggle_api:
        setup_kaggle()

    try:
        name = dataset_path.split("/")[-1]

        if is_competition:
            os.system(f"kaggle competitions download -c {name}")
        else:
            os.system(f"kaggle datasets download -d {dataset_path}")

        zip_file = f"{name}.zip"
        if unzip and os.path.exists(zip_file):
            os.system(f"unzip -q {zip_file} -d {name}")

        if delete_zip and os.path.exists(zip_file):
            os.remove(zip_file)

        print(f"✅ Successfully downloaded and extracted: {name}")

    except Exception as e:
        print(f"Error: {str(e)}")
        print("Please check the following:")
        print("- Dataset or competition name is correct")
        print("- You have accepted the competition rules if applicable")
        print("- Your Kaggle API key is valid and correctly configured")


# Example Usage
# Step 1 (optional): Set up the Kaggle API (only once per session)
# setup_kaggle()

# Step 2: Download dataset or competition files
# For datasets:
# download_kaggle_data('username/dataset-name', setup_kaggle_api=False)

# For competitions:
# download_kaggle_data('competition-name', setup_kaggle_api=False, is_competition=True)

# ============================================================================================



## dataset_splitter.py 

"""

📂 Input Dataset Structure (before splitting)

dataset/
├── class1/
│   ├── image-1.jpg
│   ├── ...
│   └── image-n.jpg
├── class2/
│   ├── image-1.jpg
│   ├── ...
│   └── image-n.jpg

============================================================

📂 Expected Output Folder Structure (after splitting)

dataset_split/
├── train/
│   └── class1/
│        ├── image-k.jpg
│        └── ...
│   ├── class2/
│   │      ├── image-l.jpg
│   │      └── ...
├── val/
│   ├── class1/
│   │      ├── image-m.jpg
│   │      └── ...
│   ├── class2/
│   │      ├── image-n.jpg
│   │      └── ...
├── test/
│   ├── class1/
│   │      ├── image-o.jpg
│   │      └── ...
│   ├── class2/
│   │      ├── image-p.jpg
│   │      └── ...

"""

# Function to split a single class folder
def split_class(
    class_dir,
    output_dir,
    ratio=(0.7, 0.2, 0.1),
    class_name=None,
    move=False,
    seed=None,
    shuffle=True,
    image_extensions=(".png", ".jpg", ".jpeg"),
    verbose=True,
):
    """
    Split a single class folder into train, val, and test folders.

    Parameters:
    - class_dir (str): Path to the class folder.
    - output_dir (str): Path where the split folders will be created.
    - ratio (tuple): Tuple of 3 values summing to 1, representing train/val/test split.
    - class_name (str): Optional custom class name. Defaults to the folder name.
    - move (bool): If True, move files instead of copying.
    - seed (int): Random seed for reproducibility.
    - shuffle (bool): If True, shuffle the images before splitting.
    - image_extensions (tuple): Tuple of image file extensions to include.
    - verbose (bool): If True, print detailed information during processing.

    Returns:
    - dict: A dictionary containing class-wise split details.
    """
    train_ratio, val_ratio, test_ratio = ratio
    assert (
        round(train_ratio + val_ratio + test_ratio, 2) == 1.0
    ), "Ratios must sum to 1.0"

    class_name = class_name or os.path.basename(class_dir)

    images = [
        file
        for file in os.listdir(class_dir)
        if file.lower().endswith(image_extensions)
    ]

    total_images = len(images)
    if total_images == 0:
        if verbose:
            print(f"No images found in class '{class_name}'.")
        return

    if verbose:
        print(f"Processing class '{class_name}' - Total images: {total_images}")

    if seed is not None:
        random.seed(seed)

    if shuffle:
        random.shuffle(images)

    train_end = int(total_images * train_ratio)
    val_end = train_end + int(total_images * val_ratio)

    splits = {}
    if train_ratio > 0:
        splits["train"] = images[:train_end]
    if val_ratio > 0:
        splits["val"] = images[train_end:val_end]
    if test_ratio > 0:
        splits["test"] = images[val_end:]

    class_details = {"class":class_name, "total":total_images, "train":0, "val":0, "test":0}

    for split_name, split_images in splits.items():
        class_details[split_name] = len(split_images)
        if not split_images:
            continue

        split_dir = os.path.join(output_dir, split_name, class_name)
        os.makedirs(split_dir, exist_ok=True)

        for image_name in split_images:
            src = os.path.join(class_dir, image_name)
            dst = os.path.join(split_dir, image_name)
            if move:
                shutil.move(src, dst)
            else:
                shutil.copy2(src, dst)

        if verbose:
            print(f"  {split_name.capitalize():5s} images: {len(split_images)}")

    if verbose:
        print()

    return class_details


# Function to split the entire dataset
def split_dataset(
    data_dir,
    output_dir,
    ratio=(0.7, 0.2, 0.1),
    move=False,
    seed=None,
    shuffle=True,
    image_extensions=(".png", ".jpg", ".jpeg"),
    verbose=True,
):
    """
    Split all class folders in a dataset directory into train, val, and test sets.

    Parameters:
    - data_dir (str): Path to the root dataset directory (each subfolder is a class).
    - output_dir (str): Path where the split folders will be created.
    - ratio (tuple): Tuple of 3 values summing to 1, representing train/val/test split.
    - move (bool): If True, move files instead of copying.
    - seed (int): Random seed for reproducibility.
    - shuffle (bool): If True, shuffle the images before splitting.
    - image_extensions (tuple): Tuple of image file extensions to include.
    - verbose (bool): If True, print detailed information during processing.

    Returns:
    - list: A list of dictionaries containing class-wise split details.
    """
    summary = []

    for class_name in os.listdir(data_dir):
        class_path = os.path.join(data_dir, class_name)
        if os.path.isdir(class_path):
            class_details = split_class(
                class_dir=class_path,
                output_dir=output_dir,
                ratio=ratio,
                class_name=class_name,
                move=move,
                seed=seed,
                shuffle=shuffle,
                image_extensions=image_extensions,
                verbose=verbose,
            )

            if class_details:
                summary.append(class_details)


# Usage Example
# if __name__ == "__main__":
#     # You can run this file directly or import the function elsewhere
#     data_dir = "input-dataset-dir"
#     output_dir = "dataset_split"

#     summary = split_dataset(
#         data_dir=data_dir,
#         output_dir=output_dir,
#         ratio=(0.8, 0.1, 0.1),  # 80% train, 10% val, 10% test
#         move=False,  # Set to True if you want to move instead of copy
#         seed=42,
#         shuffle=True,
#         image_extensions=(".jpg", ".jpeg", ".png", ".bmp"),
#         verbose=True,
#     )

# ============================================================================================
