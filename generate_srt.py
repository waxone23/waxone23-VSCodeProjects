def generate_srt(subtitles, filename="subtitles.srt"):
    with open(filename, "w", encoding="utf-8") as f:
        for i, (start, end, text) in enumerate(subtitles, start=1):
            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")
    print(f"SRT file created: {filename}")


# Format: (Start_Time, End_Time, Text)
demo_subs = [
    ("00:00:01,000", "00:00:03,000", "Welcome to the Python workflow!"),
    ("00:00:03,500", "00:00:06,000", "This subtitle was generated via code."),
]

generate_srt(demo_subs)
