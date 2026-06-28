import os

import cloudinary.uploader


class CloudinaryUploadError(Exception):

    pass


def cloudinary_is_configured():

    return all(
        os.environ.get(name)
        for name in (
            'CLOUDINARY_CLOUD_NAME',
            'CLOUDINARY_API_KEY',
            'CLOUDINARY_API_SECRET',
        )
    )


def upload_image_to_cloudinary(uploaded_file, folder):

    if not uploaded_file or not cloudinary_is_configured():

        return ''

    if hasattr(uploaded_file, 'seek'):

        uploaded_file.seek(0)

    try:

        result = cloudinary.uploader.upload(
            uploaded_file,
            folder=folder,
            resource_type='image',
        )

    except Exception as exc:

        raise CloudinaryUploadError(
            f'Cloudinary upload failed: {exc}'
        ) from exc

    return result.get('secure_url') or result.get('url') or ''
