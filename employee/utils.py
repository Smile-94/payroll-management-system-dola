from django.core.exceptions import ValidationError
from PIL import Image


def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.info_of.email,filename)


def validate_image_dimention(image):
    with Image.open(image) as img:
        width, height = img.size
        if width > 300 or height > 300:
            raise ValueError("Image height and width should be 300px or less")


def validate_image_signature_dimention(image):
    with Image.open(image) as img:
        width, height = img.size
        if width > 300 or height > 80:
            raise ValueError("Image height should be 80 and width should be 300px or less")


def validate_image_type(value):
    try:
        img = Image.open(value)
        # Check if the image is of type JPEG, PNG, or GIF
        if img.format not in ('JPEG','jpg', 'PNG',):
            raise ValidationError("Image must be of type JPEG, PNG, or GIF")

    except:
        raise ValidationError("Invalid image type")


def validate_image_file_size(value):
    try:
        # Check if the image file size is less than max_size
        max_size = 500 * 1024  # 500kb
        if value.size > max_size:
            raise ValidationError("Image size must be less than 5MB")
    except:
        raise ValidationError("Invalid image size")


def validate_signature_image_file_size(value):
    try:
        # Check if the image file size is less than max_size
        max_size = 500 * 1024  # 500kb
        if value.size > max_size:
            raise ValidationError("Image size must be less than 5MB")
    except:
        raise ValidationError("Invalid image size")
