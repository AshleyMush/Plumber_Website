import os
from werkzeug.utils import secure_filename

def save_file(file, subfolder=''):
    """
    Save an uploaded file into the 'static/uploads' directory, optionally into a subfolder.
    Returns a path starting with '/static/uploads/...', suitable for direct use in an <img> tag.

    Args:
        file: The file object from the form.
        subfolder: A subfolder within 'uploads' for organization, e.g. 'jobs_done'.

    Returns:
        str: A publicly accessible file path starting with '/static/uploads/...'
             or None if no file is provided.
    """
    if not file:
        return None

    filename = secure_filename(file.filename)
    # Full path to the uploads directory inside static
    if subfolder:
        upload_dir = os.path.join('static', 'uploads', subfolder)
    else:
        upload_dir = os.path.join('static', 'uploads')

    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)

    # Create a path accessible from the browser
    # Since 'file_path' is inside 'static', we can serve it under '/static/'
    public_path = '/static/' + os.path.relpath(file_path, 'static').replace('\\', '/')
    return public_path
