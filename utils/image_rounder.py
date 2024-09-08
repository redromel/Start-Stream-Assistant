import os
from PIL import Image, ImageDraw

import os
from PIL import Image, ImageDraw

def add_border_and_round_corners(image_path, output_path, border_size=10, corner_radius=30):
    # Open the original image
    img = Image.open(image_path).convert("RGBA")
    
    # Calculate new size with border and rounded corners
    border_size = int(border_size)
    corner_radius = int(corner_radius)
    
    # Create a new image with white background
    new_size = (img.width + 2 * (border_size + corner_radius), img.height + 2 * (border_size + corner_radius))
    new_img = Image.new("RGBA", new_size, (0, 0, 0, 0))  # White background

    # Draw rounded rectangle mask for the border area
    mask = Image.new('L', new_size, 0)
    draw = ImageDraw.Draw(mask)
    
    # Draw a rounded rectangle for the border
    draw.rounded_rectangle(
        (border_size, border_size, new_size[0] - border_size, new_size[1] - border_size),
        radius=corner_radius,
        fill=255
    )
    
    # Apply mask to the white background
    new_img.putalpha(mask)
    
    # Paste the original image onto the white background
    paste_position = (border_size + corner_radius, border_size + corner_radius)
    new_img.paste(img, paste_position, img)
    
    # Save the result
    new_img.save(output_path, format="PNG")

def process_images_in_folder(source_folder, destination_folder, border_size=10, corner_radius=30):
    """
    Processes all images in the source folder, adds a black border, and rounds the corners,
    then saves the processed images to the destination folder.
    """
    # Ensure the destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # Iterate over all files in the source folder
    for filename in os.listdir(source_folder):
        # Get the full path to the file
        source_path = os.path.join(source_folder, filename)
        
        # Check if it is a file and if it is an image
        if os.path.isfile(source_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # Define the destination path
            destination_path = os.path.join(destination_folder, f'{filename}')
            
            try:
                # Process the image: Add border and round corners
                add_border_and_round_corners(source_path, destination_path, border_size, corner_radius)
                print(f'Processed image saved to {destination_path}')
            except FileNotFoundError as e:
                print(e)
            except PermissionError:
                print(f'Permission denied while processing the file: {filename}')
            except Exception as e:
                print(f'An error occurred while processing the file {filename}: {e}')


def main():
    # source_folder = 'country_flags'
    # destination_folder = 'country_flags_rounded'
    # process_images_in_folder(source_folder, destination_folder, border_size=50, corner_radius=10)
    add_border_and_round_corners("utils/640px-Flag_of_Serbia_and_Montenegro_(1992–2006).svg.png","utils/Flag_of_Serbia_and_Montenegro_rounded.png", border_size=50, corner_radius=10)
    
if __name__ in {"__main__"}:
    main()