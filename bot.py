from PIL import Image, ImageOps
import os
import colorsys

def convert_background_to_transparent(image_path, tolerance=30):
    img = Image.open(image_path)
    img = img.convert('RGBA')
    datas = img.getdata()
    
    # Get the background color from the top-left pixel
    background_color = datas[0][:3]
    
    newData = []
    for item in datas:
        r, g, b, a = item
        
        # Check if the pixel color is close to the background color
        if (abs(r - background_color[0]) <= tolerance and 
            abs(g - background_color[1]) <= tolerance and 
            abs(b - background_color[2]) <= tolerance):
            newData.append((255, 255, 255, 0))  # Transparent
        else:
            newData.append(item)

    img.putdata(newData)
    return img

def remove_white_pixels(image_path):
    img = Image.open(image_path)
    img = img.convert('RGBA')
    datas = img.getdata()
    
    newData = []
    for item in datas:
        r, g, b, a = item
        # Check if the pixel is white
        if r > 240 and g > 240 and b > 240:
            newData.append((255, 255, 255, 0))  # Transparent
        else:
            newData.append(item)
    
    img.putdata(newData)
    img.save(image_path)
    print(f'Removed white pixels from: {os.path.basename(image_path)}')

def convert_images_to_gif(src_dir, duration=33, loop=0):
    gif_path = os.path.join(src_dir, 'output.gif')
    images = []
    
    for filename in os.listdir(src_dir):
        if filename.lower().endswith(('_transparent.png', '_resized.png')):
            img_path = os.path.join(src_dir, filename)
            img = Image.open(img_path)
            
            # Ensure the image has an alpha channel for transparency
            img = img.convert('RGBA')
            images.append(img)
    
    if images:
        images[0].save(
            gif_path, 
            save_all=True, 
            append_images=images[1:], 
            loop=loop, 
            duration=duration,  # 30 FPS = 1000 ms / 30 = 33 ms per frame
            transparency=255,  # Preserve transparency in the GIF
            disposal=2  # Clear the frame before rendering the next
        )
        print(f'All images converted to GIF: {gif_path}')

def delete_generated_files(src_dir):
    for filename in os.listdir(src_dir):
        if filename.lower().endswith(('.gif', 'merged_image.png')):
            file_path = os.path.join(src_dir, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f'Deleted {filename}')
    for filename in os.listdir(src_dir):
        if filename.lower().endswith('_transparent.png'):
            file_path = os.path.join(src_dir, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f'Deleted {filename}')

def add_border_to_images(src_dir, border_size=1, color='black'):
    for filename in os.listdir(src_dir):
        if filename.lower().endswith(('_transparent.png', '_resized.png')):
            img_path = os.path.join(src_dir, filename)
            img = Image.open(img_path)
            img_with_border = ImageOps.expand(img, border=border_size, fill=color)
            img_with_border.save(img_path)
            print(f'Added border to {filename}')

def resize_images(src_dir, size, resample_filter=Image.LANCZOS):
    for filename in os.listdir(src_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.webp', '.png')):
            img_path = os.path.join(src_dir, filename)
            img = Image.open(img_path)
            img = img.resize(size, resample_filter)
            
            if filename.lower().endswith('_transparent.png'):
                output_path = img_path
            else:
                output_filename = os.path.splitext(filename)[0] + '_resized.png'
                output_path = os.path.join(src_dir, output_filename)
            
            img.save(output_path)
            print(f'Resized {filename} to {os.path.basename(output_path)}')

def merge_images_into_one(src_dir):
    output_path = os.path.join(src_dir, 'merged_image.png')
    images = []
    
    for filename in os.listdir(src_dir):
        if filename.lower().endswith(('_transparent.png', '_resized.png')):
            img_path = os.path.join(src_dir, filename)
            images.append(Image.open(img_path))
    
    if images:
        # Calculate the total width and max height for the merged image
        total_width = sum(img.width for img in images)
        max_height = max(img.height for img in images)
        
        # Create a new blank image with a transparent background
        merged_image = Image.new('RGBA', (total_width, max_height), (255, 255, 255, 0))
        
        # Paste each image side by side
        x_offset = 0
        for img in images:
            merged_image.paste(img, (x_offset, 0))
            x_offset += img.width
        
        merged_image.save(output_path)
        print(f'All images merged into one: {output_path}')

def process_directory():
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    
    if not os.path.exists(src_dir):
        os.makedirs(src_dir)

    # Ask if the user wants to convert the background of the images
    user_input = input("Do you want to convert the background of the images to transparent? (yes/no): ").strip().lower()
    if user_input == 'yes':
        # Ask for the tolerance value
        while True:
            try:
                tolerance = int(input("Enter the tolerance for background conversion (0-255): "))
                if 0 <= tolerance <= 255:
                    break
                else:
                    print("Please enter a value between 0 and 255.")
            except ValueError:
                print("Please enter a valid number.")
        
        for filename in os.listdir(src_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.webp', '.png')):
                input_path = os.path.join(src_dir, filename)
                output_filename = os.path.splitext(filename)[0] + '_transparent.png'
                output_path = os.path.join(src_dir, output_filename)
                
                img = convert_background_to_transparent(input_path, tolerance)
                img.save(output_path, 'PNG')
                print(f'Converted {filename} to {output_filename}')

        # Ask if the user wants to keep the original files
        keep_originals = input("Do you want to keep the original files? (yes/no): ").strip().lower() == 'yes'
        if not keep_originals:
            for filename in os.listdir(src_dir):
                if filename.lower().endswith(('.jpg', '.jpeg', '.webp', '.png')) and not filename.lower().endswith('_transparent.png'):
                    os.remove(os.path.join(src_dir, filename))
                    print(f'Deleted original: {filename}')
    
    # Ask if the user wants to convert all images to GIF
    user_input = input("Do you want to convert all images to a single GIF? (yes/no): ").strip().lower()
    if user_input == 'yes':
        while True:
            try:
                duration = int(input("Enter the duration for each frame (in milliseconds): "))
                break
            except ValueError:
                print("Please enter a valid number.")
        while True:
            try:
                loop = int(input("Enter the number of loops (0 for infinite): "))
                break
            except ValueError:
                print("Please enter a valid number.")
        convert_images_to_gif(src_dir, duration=duration, loop=loop)
    
    # Ask if the user wants to merge all images into one
    user_input = input("Do you want to merge all converted images into a single image? (yes/no): ").strip().lower()
    if user_input == 'yes':
        merge_images_into_one(src_dir)

    # Ask if the user wants to resize images
    user_input = input("Do you want to resize all converted images? (yes/no): ").strip().lower()
    if user_input == 'yes':
        while True:
            try:
                width = int(input("Enter the width: "))
                height = int(input("Enter the height: "))
                break
            except ValueError:
                print("Please enter a valid number.")
        print("Choose a resampling filter:")
        print("1. Nearest")
        print("2. Lanczos")
        print("3. Bilinear")
        print("4. Bicubic")
        print("5. Box")
        print("6. Hamming")
        while True:
            try:
                filter_choice = int(input("Enter the number of the filter: "))
                if 1 <= filter_choice <= 6:
                    break
                else:
                    print("Please enter a number between 1 and 6.")
            except ValueError:
                print("Please enter a valid number.")
        
        filters = [Image.NEAREST, Image.LANCZOS, Image.BILINEAR, Image.BICUBIC, Image.BOX, Image.HAMMING]
        resample_filter = filters[filter_choice - 1]

        resize_images(src_dir, size=(width, height), resample_filter=resample_filter)

    # Ask if the user wants to add a border to images
    user_input = input("Do you want to add a border to all converted images? (yes/no): ").strip().lower()
    if user_input == 'yes':
        border_color = input("Enter the border color (e.g., black, red, #FF0000): ")
        while True:
            try:
                border_size = int(input("Enter the border size (in pixels): "))
                break
            except ValueError:
                print("Please enter a valid number.")
        add_border_to_images(src_dir, color=border_color, border_size=border_size)

    # Ask if the user wants to delete generated files
    user_input = input("Do you want to delete all generated files (transparent images, gif, merged image)? (yes/no): ").strip().lower()
    if user_input == 'yes':
        delete_generated_files(src_dir)
    
    # Ask if the user wants to remove white pixels
    user_input = input("Do you want to remove white pixels from all converted images? (yes/no): ").strip().lower()
    if user_input == 'yes':
        for filename in os.listdir(src_dir):
            if filename.lower().endswith(('_transparent.png', '_resized.png')):
                remove_white_pixels(os.path.join(src_dir, filename))

    # Ask if the user wants to delete the src folder
    user_input = input("Do you want to delete the src folder? (yes/no): ").strip().lower()
    if user_input == 'yes':
        import shutil
        shutil.rmtree(src_dir)
        print('Deleted src folder')

if __name__ == '__main__':
    process_directory()