import os
from google.colab import files

def setup_kaggle():
    """Install Kaggle API and set up credentials."""
    # Upload kaggle.json    
    print("Please upload your 'kaggle.json' file:")
    uploaded = files.upload()
    
    if 'kaggle.json' not in uploaded:
        raise FileNotFoundError("Failed to upload kaggle.json - please download it from Kaggle account settings")
    
    # Move and set permissions
    !mkdir -p ~/.kaggle
    !mv kaggle.json ~/.kaggle/
    !chmod 600 ~/.kaggle/kaggle.json
    print("Kaggle API successfully configured!")

def download_kaggle_data(dataset_path, setup_kaggle_api=True, is_competition=False, unzip=True, delete_zip=True):
    """
    Download and extract Kaggle dataset or competition files.
    
    Args:
        dataset_path (str): Format 'username/dataset-name' or 'competition-name'
        setup_kaggle_api (bool): True if you've already set up the Kaggle API
        is_competition (bool): True for competitions, False for datasets
        unzip (bool): Whether to unzip the dataset after download (default True)
        delete_zip (bool): Whether to delete the zip file after extraction (default True)
    """
    if setup_kaggle_api:
        setup_kaggle()

    try:
        username, dataset_name = dataset_path.split("/")[-2:]

        # Download
        if is_competition:
            !kaggle competitions download -c {dataset_name}
        else:
            !kaggle datasets download -d {username}/{dataset_name}
                
        # Unzip if the option is enabled
        if unzip:
            !unzip -q {dataset_name}.zip -d {dataset_name}
        
        # Clean up zip file if the option is enabled
        if delete_zip:
            !rm {dataset_name}.zip
        
        print(f"Successfully downloaded and extracted {dataset_name}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Make sure:")
        print("- The dataset/competition name is correct")
        print("- You have accepted competition rules (if applicable)")
        print("- Your Kaggle API key is valid")


# Example usage:
# 1. Set up Kaggle API (run this only once per session)
# setup_kaggle()

# 2. Download a dataset or competition data
# For datasets:
# download_kaggle_data('<username/dataset-name>', setup_kaggle_api=False)

# For competitions:
# download_kaggle_data('<competitions-name>', setup_kaggle_api=False, is_competition=True)