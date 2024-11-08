from PIL import Image

def rotate_gif(input_path, output_path):
    with Image.open(input_path) as img:
        frames = []
        for frame in range(img.n_frames):
            img.seek(frame)
            rotated_frame = img.rotate(-90, expand=True)
            frames.append(rotated_frame)

        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=img.info['duration'],
            loop=0
        )
    print(f"Rotated GIF saved as {output_path}")