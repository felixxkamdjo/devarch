import os
import uuid


BASE_STORAGE = "storage"


def allowed_extension(filename, allowed_types):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_types


def save_file(file_data, filename, folder="files"):
    """
    Saves file to disk with UUID filename
    """

    file_ext = filename.rsplit(".", 1)[1].lower()
    new_filename = f"{uuid.uuid4()}.{file_ext}"

    folder_path = os.path.join(BASE_STORAGE, folder)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, new_filename)

    with open(file_path, "wb") as f:
        f.write(file_data)

    return {
        "filename": new_filename,
        "path": file_path,
        "url": f"/{folder}/{new_filename}"
    }


def delete_file(filename, folder="files"):

    file_path = os.path.join(BASE_STORAGE, folder, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return True

    return False


def get_file_path(filename, folder="files"):

    return os.path.join(BASE_STORAGE, folder, filename)