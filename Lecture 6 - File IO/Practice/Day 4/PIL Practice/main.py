from PIL import Image, ImageDraw, ImageFont
# Image is for Opening and closing images
# ImageDraw is for drawing on images
# ImageFont is for adding text to images

# Open the image
img = Image.open("input.jpg")

# check image properties
print("Format:", img.format)
print("Size:", img.size)
print("Mode:", img.mode)


# Crop an image
cropped = img.crop((100, 100, 1400, 1400))
cropped.format = img.format
cropped.save("cropped.jpg")
print("Format:", cropped.format)
print("Size:", cropped.size)
print("Mode:", cropped.mode)

# Resize an image
resized = img.resize((400, 400))
resized.format = img.format
resized.save("resized.jpg")
print("Format:", resized.format)
print("Size:", resized.size)
print("Mode:", resized.mode)

# Rotate an image
rotated = img.rotate(45)
rotated.save("rotated.jpg")

# Convert an image to grayscale
gray = img.convert("L")
gray.save("grayscale.jpg")

# Flip an image horizontally
flipped = img.transpose(Image.FLIP_LEFT_RIGHT)
flipped.save("flipped.jpg")

# Add text to an image
draw = ImageDraw.Draw(img)
draw.text(
    (50, 50), 
    "Sample Text", 
    fill="red"
)

img.save("text_added.jpg")

# close an image
img.close()
cropped.close()
resized.close()
gray.close()
flipped.close()
draw.close()