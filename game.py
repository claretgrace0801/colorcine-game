import json
import random

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from PIL import Image, ImageDraw, ImageFont

def cropped(image_path):
    # Open the image file
    img = Image.open(image_path)

    # Define the coordinates of the crop box (left, upper, right, lower)
    crop_box = (20, 15, 570, 710)  # Example coordinates

    # Crop the image using the crop box
    cropped_img = img.crop(crop_box)

    # Optionally, save the cropped image to a new file
    cropped_img = cropped_img.convert('RGB')
    return cropped_img
    # cropped_img.save('/content/cropped_image.jpg')


NO_IMAGES = 3

with open('map.json', 'r') as file:
    data = json.load(file)
items = list(data.items())

picked_images = random.sample(items, NO_IMAGES)

random_indices = list(range(NO_IMAGES))
random.shuffle(random_indices)

random_names = [picked_images[i][0] for i in random_indices]

shuffled_images = [(random_names[i], picked_images[i][1]) for i in range(NO_IMAGES)]

def game(correct = False):

    # Create three PIL Image objects (for demonstration purposes, using solid colors)
    img1,img2,img3 = [cropped(img[1]) for img in shuffled_images]
    if not correct:
        labels = [img[0] for img in shuffled_images]
    else:
        labels = [img[0] for img in picked_images]

    # Define font size and font (default font)
    font_size = 20
    try:
        # Try to use a specific font if available
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Fallback to the default PIL font if specific font is not found
        font = ImageFont.load_default()

    # Calculate the total width and the maximum height (with added space for text) of the final image
    total_width = img1.width + img2.width + img3.width
    max_height = max(img1.height, img2.height, img3.height) + font_size + 10  # Add space for the text

    # Create a new image with the calculated total width and maximum height
    combined_img = Image.new('RGB', (total_width, max_height), (255, 255, 255))  # Use a white background

    # Function to paste an image and its label into the combined image
    def paste_with_label(image, label, position):
        # Paste the image
        combined_img.paste(image, position)
        
        # Create a drawing context
        draw = ImageDraw.Draw(combined_img)
        
        # Calculate text position (below the image)
        text_x = position[0] + (image.width - font.getsize(label)[0]) / 2
        text_y = position[1] + image.height + 5
        
        # Add the text label
        draw.text((text_x, text_y), label, fill=(0, 0, 0), font=font)

    # Paste each image and its label
    paste_with_label(img1, labels[0], (0, 0))
    paste_with_label(img2, labels[1], (img1.width, 0))
    paste_with_label(img3, labels[2], (img1.width + img2.width, 0))

    return combined_img

game(False).show()
game(True).save('correct_answer.jpg')