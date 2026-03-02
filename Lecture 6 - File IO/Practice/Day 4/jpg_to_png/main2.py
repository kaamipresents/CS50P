import os
from PIL import Image

def get_directoy_files():
    global image_folder
    image_folder = 'images'
    image_files = os.listdir(image_folder)
    return image_files

def jpg_images_opener(image_file):
    if image_file.endswith(".jpg"):
        image_path = os.path.join(image_folder, image_file)
        img = Image.open(image_path)
        return img
    return None

def main():
    # list files in images folder
    count = 0
    image_files = get_directoy_files()
    print("Image files in the folder:")
    for image_file in image_files:
        img = jpg_images_opener(image_file)
        if img is not None:
            file, ext = os.path.splitext(image_file) 
            png_file = file + '.png'
            img.save(os.path.join('converted_images', png_file), 'PNG')
            count += 1
            print(f"Converted '{image_file}' to '{png_file}'")
    print(f"Total {count} images converted.")
    print("Conversion completed.")

if __name__ == "__main__":
    main()
