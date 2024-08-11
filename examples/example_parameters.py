from casares.server import casares_post, run_server
from PIL import Image

@casares_post("obj", "text")
def obj_vertices(obj,scale=1.0,translate_y=0.0):
    """
    asset is a trimesh object, this function returns a text response with the vertices of the object
    """

    print(scale)
    print(translate_y)

    try:
        # Convert the list of vertices to a string
        output_txt = str(scale) + "\n" + str(translate_y) + "\n"
        vertices_string = "\n".join([f"{vertex[0]} {vertex[1]} {vertex[2]}" for vertex in obj.vertices])
        return output_txt+ vertices_string

    except Exception as e:
        print(f"Error occurred during rendering: {e}")
        return None


if __name__ == "__main__":
    run_server()