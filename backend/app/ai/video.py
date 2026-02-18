from pathlib import Path
import subprocess


def render_video(audio_path: str, thumbnail_path: str, output_path: str, duration: int) -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
        "-i",
        thumbnail_path,
        "-i",
        audio_path,
        "-t",
        str(duration),
        "-vf",
        "scale=1920:1080",
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-pix_fmt",
        "yuv420p",
        "-shortest",
        output_path,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path
