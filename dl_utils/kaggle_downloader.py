import os
import shutil
from pathlib import Path
from google.colab import files

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
