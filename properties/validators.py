from pathlib import Path

from django.core.exceptions import ValidationError


MAX_IMAGE_UPLOAD_SIZE = 5 * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = {
    '.jpg',
    '.jpeg',
    '.png',
    '.webp',
}
ALLOWED_IMAGE_CONTENT_TYPES = {
    'image/jpeg',
    'image/png',
    'image/webp',
}


def validate_image_upload(uploaded_file):

    if not uploaded_file:

        return

    if uploaded_file.size > MAX_IMAGE_UPLOAD_SIZE:

        raise ValidationError(
            'Image must be 5 MB or smaller.'
        )

    extension = Path(
        uploaded_file.name
    ).suffix.lower()

    if extension not in ALLOWED_IMAGE_EXTENSIONS:

        raise ValidationError(
            'Upload a JPG, PNG, or WEBP image.'
        )

    content_type = getattr(
        uploaded_file,
        'content_type',
        ''
    )

    if (
        content_type
        and content_type not in ALLOWED_IMAGE_CONTENT_TYPES
    ):

        raise ValidationError(
            'Upload a valid JPG, PNG, or WEBP image.'
        )
