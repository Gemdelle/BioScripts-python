import os

import imageio

# insert gif name here
gif_name = "harvest-mushroom"
gif_path = f"../assets/gifs/{gif_name}.gif"
frames_folder = f"../assets/gifs/frames/{gif_name}"

# Ensure frames folder exists
os.makedirs(frames_folder, exist_ok=True)
print(gif_path)
# Read GIF frames and save as separate images
with imageio.get_reader(gif_path) as reader:
    for i, frame in enumerate(reader):
        # Create file path for each frame
        frame_path = os.path.join(frames_folder, f'{gif_name}_{i}.png')

        # Save frame as PNG
        imageio.imwrite(frame_path, frame, format='PNG')