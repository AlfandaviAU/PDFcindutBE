import zipfile

def get_root_folder_name(zip_filepath):
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        # Extract the first entry to get the root folder
        root_folder = zip_ref.namelist()[0]
        if root_folder.endswith('/'):
            root_folder = root_folder[:-1]  # Remove trailing slash
        return root_folder

# Usage
zip_filepath = 'Cindut.zip'  # Provide the path to your ZIP file
root_folder_name = get_root_folder_name(zip_filepath)
print("Root folder name:", root_folder_name)
