from PIL import Image
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

if __name__ == '__main__':
    process_directory()