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

def convert_images_to_gif(src_dir):
    gif_path = os.path.join(src_dir, 'output.gif')
    images = []
    
    for filename in os.listdir(src_dir):
        if filename.lower().endswith('_transparent.png'):
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
            loop=0, 
            duration=33,  # 30 FPS = 1000 ms / 30 = 33 ms per frame
            transparency=255,  # Preserve transparency in the GIF
            disposal=2  # Clear the frame before rendering the next
        )
        print(f'All images converted to GIF: {gif_path}')

def merge_images_into_one(src_dir):
    output_path = os.path.join(src_dir, 'merged_image.png')
    images = []
    
    for filename in os.listdir(src_dir):
        if filename.lower().endswith('_transparent.png'):
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
    
    for filename in os.listdir(src_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.webp', '.png')):
            input_path = os.path.join(src_dir, filename)
            output_filename = os.path.splitext(filename)[0] + '_transparent.png'
            output_path = os.path.join(src_dir, output_filename)
            
            img = convert_background_to_transparent(input_path)
            img.save(output_path, 'PNG')
            print(f'Converted {filename} to {output_filename}')
            
            # Delete the original file
            os.remove(input_path)
            print(f'Deleted original: {filename}')
    
    # Ask if the user wants to convert all images to GIF
    user_input = input("Do you want to convert all images to a single GIF? (yes/no): ").strip().lower()
    if user_input == 'yes':
        convert_images_to_gif(src_dir)
    
    # Ask if the user wants to merge all images into one
    user_input = input("Do you want to merge all converted images into a single image? (yes/no): ").strip().lower()
    if user_input == 'yes':
        merge_images_into_one(src_dir)

if __name__ == '__main__':
    process_directory()