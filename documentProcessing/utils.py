import os


def delete_image(imageName):
    image_path = "processing_image/" + imageName

    try:
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"deleted '{imageName}' ")
        else:
            print(f"'{imageName}' not exist.")
    except Exception as e:
        print(f"erro: {str(e)}")
