import os
import subprocess


def apply_lut_to_folder(input_dir, lut_path, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Standard video extensions
    valid_extensions = (".mp4", ".mov", ".mxf", ".mkv")

    print(f"--- Starting Batch Grade ---")
    print(f"Using LUT: {os.path.basename(lut_path)}")

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(valid_extensions):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"GRADED_{filename}")

            # FFmpeg Command
            # 'lut3d' is the filter that applies the .cube file
            cmd = [
                "ffmpeg",
                "-i",
                input_path,
                "-vf",
                f"lut3d={lut_path}",
                "-c:v",
                "libx264",  # High quality H.264
                "-pix_fmt",
                "yuv420p",  # Ensure compatibility
                "-crf",
                "18",  # High quality (lower is better, 18-23 is standard)
                "-c:a",
                "copy",  # Keep original audio
                output_path,
                "-y",  # Overwrite if exists
            ]

            print(f"Processing: {filename}...")

            try:
                subprocess.run(cmd, check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                print(f"Error processing {filename}: {e.stderr.decode()}")

    print(f"\nDone! All files saved to: {output_dir}")


# --- CONFIGURATION ---
input_folder = r"C:\MyProject\RAW_Footage"
lut_file = r"C:\MyProject\LUTs\teal_orange.cube"
output_folder = r"C:\MyProject\Cinematic_Exports"

if __name__ == "__main__":
    apply_lut_to_folder(input_folder, lut_file, output_folder)
