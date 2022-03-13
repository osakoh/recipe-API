import os
import uuid


def recipe_image_file_path(instance, filename):
    """ Generate file path for new recipe image """
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join("uploads/recipe/", filename)
