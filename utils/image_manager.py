from PIL import Image
import os

class ImageManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ImageManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """
        Initialize the ImageManager.
        """
        if not self._initialized:
            self.images = {}
            self._initialized = True

    def add_image(self, file_path, resize_to=None):
        """
        Add an image to the manager from a specified file path with an optional resize.
        :param file_path: Path to the image file.
        :param resize_to: Tuple specifying the target size to resize the image (width, height).
        """
        if os.path.exists(file_path) and file_path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            try:
                image = Image.open(file_path)
                if resize_to:
                    image = image.resize(resize_to)
                filename = os.path.basename(file_path)
                self.images[filename] = (image, file_path)
            except IOError:
                print(f"Error loading image {file_path}")
        else:
            print(f"Invalid file path or unsupported file type: {file_path}")

    def get_image(self, filename):
        """
        Get a preloaded image by filename.
        :param filename: Name of the image file.
        :return: Tuple of Image object and file path, or None if not found.
        """
        return self.images.get(filename)[0]

    def list_images(self):
        """
        List all preloaded image filenames.
        :return: List of image filenames.
        """
        return list(self.images.keys())