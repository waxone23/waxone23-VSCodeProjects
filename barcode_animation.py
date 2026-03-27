import cv2
import numpy as np
import random


def create_barcode_animation():
    # 1. Video Configuration (1080p)
    width, height = 1920, 1080
    fps = 60
    output_file = "barcode_construction.mp4"

    # Define the codec and create VideoWriter object
    # 'mp4v' is standard for .mp4 files
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # 2. Initialize a blank white canvas
    # (Height, Width, Channels) - 255 is white
    canvas = np.full((height, width, 3), 255, dtype=np.uint8)

    print(f"Generating animation at {width}x{height}...")

    x_cursor = 0
    # Keep adding lines until we fill the width of the frame
    while x_cursor < width:
        # Randomly choose line weights to simulate a real barcode
        # Weights are in pixels
        line_weight = random.choice([2, 4, 8, 12, 20])
        gap = random.choice([2, 4, 8])

        # Draw the black vertical line
        # cv2.rectangle(image, top_left, bottom_right, color, thickness)
        # thickness=-1 fills the rectangle
        cv2.rectangle(
            canvas, (x_cursor, 0), (x_cursor + line_weight, height), (0, 0, 0), -1
        )

        # 3. Animation Logic
        # We write the current state of the canvas to the video file
        # To make it look like it's "building," we write 1 frame per line added
        out.write(canvas)

        # Advance the cursor
        x_cursor += line_weight + gap

    # 4. Final Hold
    # Keep the finished barcode on screen for 3 seconds (60 fps * 3)
    for _ in range(fps * 3):
        out.write(canvas)

    # Release everything
    out.release()
    print(f"Success! Animation saved as: {output_file}")


if __name__ == "__main__":
    create_barcode_animation()
