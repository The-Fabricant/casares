from casares.server import casares_post, run_server
from PIL import Image

@casares_post("obj", "image")
def frontal_view(obj,scale=50,translate_y=0):
    """
    asset is a trimesh object, this function just returns a cyan flat image
    """
    image_size = (800, 800)

    print(obj.vertices)
    print(obj.faces)

    # Load the trimesh asset
    print(scale)
    print(translate_y)

    try:
        # Create a blank image just for testing
        image = Image.new('RGB', image_size, color='cyan')

        return image

    except Exception as e:
        print(f"Error occurred during rendering: {e}")
        return None


if __name__ == "__main__":
    run_server()