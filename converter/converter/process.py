import cv2
import numpy as np
from PIL import Image

def process_frame_atkinson(frame, target_width, target_height, threshold):
    image = np.array(frame)
    original_height, original_width = image.shape[:2]

    scale = min(target_width / original_width, target_height / original_height)
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)
    resized_image = cv2.resize(image, (new_width, new_height))

    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    # Apply modified Atkinson dithering
    for y in range(new_height):
        for x in range(new_width):
            old_pixel = gray_image[y, x]
            new_pixel = 255 if old_pixel > threshold else 0
            gray_image[y, x] = new_pixel
            if old_pixel > new_pixel:
                error = old_pixel - new_pixel
            else:
                error = 0

            # Distribute a smaller portion of the error to neighboring pixels
            diffusion_factor = 0.75  
            if x + 1 < new_width:
                gray_image[y, x + 1] = min(255, max(0, gray_image[y, x + 1] + error * (1 / 8) * diffusion_factor))
            if x + 2 < new_width:
                gray_image[y, x + 2] = min(255, max(0, gray_image[y, x + 2] + error * (1 / 8) * diffusion_factor))
            if y + 1 < new_height:
                if x > 0:
                    gray_image[y + 1, x - 1] = min(255, max(0, gray_image[y + 1, x - 1] + error * (1 / 8) * diffusion_factor))
                gray_image[y + 1, x] = min(255, max(0, gray_image[y + 1, x] + error * (1 / 8) * diffusion_factor))
                if x + 1 < new_width:
                    gray_image[y + 1, x + 1] = min(255, max(0, gray_image[y + 1, x + 1] + error * (1 / 8) * diffusion_factor))
            if y + 2 < new_height:
                gray_image[y + 2, x] = min(255, max(0, gray_image[y + 2, x] + error * (1 / 8) * diffusion_factor))

    # gray_image = 255 - gray_image    
    # Create a black image with the target dimensions
    output_image = np.zeros((target_height, target_width, 3), dtype=np.uint8)
    # white 
    # output_image = np.ones((target_height, target_width, 3), dtype=np.uint8) * 255


    x_offset = (target_width - new_width) // 2
    y_offset = (target_height - new_height) // 2

    output_image[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)

    return output_image


def process_frame_edges(frame, target_width, target_height):
    image = np.array(frame)
    original_height, original_width = image.shape[:2]

    scale = min(target_width / original_width, target_height / original_height)
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)
    resized_image = cv2.resize(image, (new_width, new_height))

    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    # stack overflow edge detection i found
    # seems to work better with some images 

    # thresh = cv2.threshold(gray_image, 80, 255, cv2.THRESH_BINARY)[1]
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    # dilate = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)
    # edges = cv2.absdiff(dilate, thresh)

    # Create a black image with the target dimensions
    output_image = np.zeros((target_height, target_width, 3), dtype=np.uint8)

    # Calculate the position to place the edge-detected image on the black image
    x_offset = (target_width - new_width) // 2
    y_offset = (target_height - new_height) // 2

    # Perform edge detection using the Canny algorithm
    edges = cv2.Canny(gray_image, threshold1=260, threshold2=450)

    # Place the edge-detected image on the black image
    output_image[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    return output_image

def process_gif(input_path, output_path, target_width, target_height, threshold, speed):
    # Open the GIF using PIL
    with Image.open(input_path) as img:
        frames = []
        # Iterate through each frame in the GIF
        for frame in range(img.n_frames):
            img.seek(frame)
            processed_frame = process_frame_atkinson(img.convert("RGB"), target_width, target_height, threshold)
            frames.append(Image.fromarray(processed_frame))

        original_duration = img.info.get('duration', 100)
        new_durations = [int(original_duration / speed) for _ in frames]

        # Save the processed frames as a new GIF with modified speeds
        frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=new_durations, loop=0)
        return original_duration