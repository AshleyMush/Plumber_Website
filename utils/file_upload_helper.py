import os
from werkzeug.utils import secure_filename

def save_file(file, base_folder='static/uploads', subfolder=''):
    """
    Save the uploaded file to the specified folder and return its relative path.

    Args:
        file: The file object from the form.
        base_folder: The base folder where files should be stored.
        subfolder: A subfolder within the base folder for organization.

    Returns:
        str: The relative path to the saved file or None if no file is provided.
    """
    if file:
        filename = secure_filename(file.filename)
        relative_path = os.path.join(base_folder, subfolder, filename).replace("\\", "/")
        full_path = os.path.join(relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        file.save(full_path)
        return relative_path
    return None
