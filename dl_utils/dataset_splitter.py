import os
import shutil
import random


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
# Usage Example
if __name__ == "__main__":
    # You can run this file directly or import the function elsewhere
    data_dir = "input-dataset-dir"
    output_dir = "dataset_split"

    summary = split_dataset(
        data_dir=data_dir,
        output_dir=output_dir,
        ratio=(0.8, 0.1, 0.1),  # 80% train, 10% val, 10% test
        move=False,  # Set to True if you want to move instead of copy
        seed=42,
        shuffle=True,
        image_extensions=(".jpg", ".jpeg", ".png", ".bmp"),
        verbose=True,
    )
