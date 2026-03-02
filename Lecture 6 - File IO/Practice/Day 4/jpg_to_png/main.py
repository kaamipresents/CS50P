# Image Format Converter (JPG → PNG)

from PIL import Image
def convert_jpg_to_png(jpg_file_path, png_file_path):
    try:
        # Open the JPG image
        jpg_image = Image.open(jpg_file_path)

        # Convert the JPG image to PNG
        jpg_image.save(png_file_path, 'PNG')
        print(f"Successfully converted '{jpg_file_path}' to '{png_file_path}'")
    except Exception as e:
        print(f"Error: {e}")    
# Example usage
jpg_file = '1.jpg'  # Replace with your JPG file path
png_file = 'converted_images/1.png'  # Replace with the desired output PNG file path
convert_jpg_to_png(jpg_file, png_file)

