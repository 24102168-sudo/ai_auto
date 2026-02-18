from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def create_thumbnail(title: str, output_path: str) -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (1920, 1080), color=(18, 18, 30))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((120, 500), title[:80], fill=(215, 180, 255), font=font)
    image.save(output_path)
    return output_path
