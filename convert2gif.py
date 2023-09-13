import subprocess
import sys
from pathlib import Path
from typing import List


def convert(input_file: Path) -> None:
    """
    Convert video file to animated gif
    :param input_file: Video file to be converted
    """
    # Check if input file exists
    if not input_file.exists():
        print(f"Input file {input_file.name} does not exist")
        return
    
    print(f"Converting {input_file.name} to animated gif...")

    # Set up output file names
    gif_path = input_file.with_suffix(".gif")

    try:
        # Call ffmpeg to convert video to gif
        subprocess.call([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i",
            input_file.__str__(),
            "-vf", f"split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
            "-loop",
            "0",
            gif_path.__str__()
        ])
        print(f"Converted {input_file.name} to {gif_path} successfully.")
    except Exception as e:
        print(f"Error converting {input_file.name} to animated gif: {e}")


def main():
    if len(sys.argv) < 2:
        print("Please provide a video file to convert")
        return

    video = Path(sys.argv[1])

    if not video.exists():
        print(f"Video file {video.name} does not exist")
        return

    video = video.resolve()

    convert(input_file=video)


main()
