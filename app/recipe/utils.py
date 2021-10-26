import os
import uuid


def recipe_image_file_path(instance, filename: str):
    """Genereta file path to new recipe image"""
    extension = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{extension}"

    return os.path.join("uploads/recipe/", filename)
