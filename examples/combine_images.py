from casares.server import casares_post_images, run_server
from PIL import Image

@casares_post_images
def combine_images(images):

    image1, image2 = images
    """
    Combine two images into one and return the result.
    """
    # An example image processing operation: merge images side by side
    total_width = image1.width + image2.width
    max_height = max(image1.height, image2.height)
    new_image = Image.new('RGB', (total_width, max_height))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1.width, 0))
    return new_image

if __name__ == "__main__":
    run_server()