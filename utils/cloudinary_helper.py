import os
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Configure Cloudinary with environment variables for security
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)


def upload_image_to_cloudinary(file, public_id=None, folder=None):
    """
    Upload an image to Cloudinary and return the secure URL.

    Args:
        file: File object (e.g., request.files['file']).
        public_id: (Optional) Unique public ID for the uploaded image.
        folder: (Optional) Folder in Cloudinary to organize the image.

    Returns:
        dict: Cloudinary upload result containing the secure URL and other details.
    """
    upload_options = {}
    if public_id:
        upload_options["public_id"] = public_id
    if folder:
        upload_options["folder"] = folder

    return cloudinary.uploader.upload(file, **upload_options)
