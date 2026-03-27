import tkinter as tk
import math
import os
from PIL import ImageGrab, Image  # Requires: pip install pillow


class AnimatedCircles:
    def __init__(self, root):
        self.root = root
        self.root.title("Animated Concentric Circles")

        self.canvas_size = 500
        self.canvas = tk.Canvas(
            root,
            width=self.canvas_size,
            height=self.canvas_size,
            bg="#fdf6e3",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.colors = ["#f9eb4e", "#fccb3e", "#f76b1c", "#c23636", "#1b0026"]
        self.num_circles = len(self.colors)
        self.base_radii = [200, 160, 120, 80, 40]

        self.angle = 0

        # GIF Export variables
        self.frames = []
        self.max_frames = 120  # Total frames to capture
        self.is_recording = True

        self.animate()

    def animate(self):
        self.canvas.delete("all")
        center = self.canvas_size / 2

        # Core animation logic
        for i in range(self.num_circles):
            phase_offset = i * 0.5
            radius = self.base_radii[i] + (math.sin(self.angle + phase_offset) * 10)

            # Draw circles
            self.canvas.create_oval(
                center - radius,
                center - radius,
                center + radius,
                center + radius,
                fill=self.colors[i],
                outline="",
            )

        self.angle += 0.1

        # --- RECORDING STEP ---
        if self.is_recording and len(self.frames) < self.max_frames:
            self.root.update()  # Ensure canvas is drawn
            x = self.root.winfo_rootx()
            y = self.root.winfo_rooty()
            w = self.root.winfo_width()
            h = self.root.winfo_height()

            # Grab window area and store in memory
            img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            self.frames.append(img)

            if len(self.frames) % 20 == 0:
                print(f"Captured {len(self.frames)}/{self.max_frames} frames...")
        elif len(self.frames) == self.max_frames:
            print("Recording Finished! CLOSE window to save GIF.")
            self.is_recording = False

        self.root.after(30, self.animate)

    def save_gif(self):
        if self.frames:
            print("Processing GIF... please wait.")
            self.frames[0].save(
                "concentric_circles.gif",
                save_all=True,
                append_images=self.frames[1:],
                duration=30,  # Match the .after() speed
                loop=0,
                optimize=True,
            )
            print("Successfully saved as 'concentric_circles.gif'!")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AnimatedCircles(root)

    # Trigger save when window is closed
    root.protocol("WM_DELETE_WINDOW", app.save_gif)
    root.mainloop()
