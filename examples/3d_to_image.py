from casares.server import casares_post_obj, run_server
from PIL import Image
import trimesh
from io import BytesIO


# @casares_post_obj
def frontal_view(asset):
    """
    asset is a trimesh object
    """
    image_size = (800, 800)

    asset1 = asset

    # Create a scene with the mesh
    scene = trimesh.Scene([asset1])

    # Set up the camera at a frontal position
    camera_distance = asset.extents.max() * 2.5
    scene.camera_transform = trimesh.transformations.translation_matrix([0, 0, camera_distance])

    try:
        # Use offscreen rendering mode to avoid issues with event loops on macOS
        png_data = scene.save_image(resolution=image_size, visible=True)

        # Convert PNG data to an image
        image = Image.open(BytesIO(png_data))
        # image = Image.new('RGB', image_size)
        
        output_path = "output.jpg"
        image.save(output_path, format='JPEG')

        return output_path

    except Exception as e:
        print(f"Error occurred during rendering: {e}")
        return None
    


if __name__ == "__main__":
    frontal_view(trimesh.load("rotated_mesh.obj"))
    # run_server()