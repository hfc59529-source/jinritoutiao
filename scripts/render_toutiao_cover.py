from pathlib import Path
import argparse

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps


CANVAS = (1672, 941)
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"


def fit_font(draw, text, max_width, start_size, stroke_width=0):
    size = start_size
    while size >= 56:
        font = ImageFont.truetype(FONT, size)
        box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
        if box[2] - box[0] <= max_width:
            return font
        size -= 4
    return ImageFont.truetype(FONT, 56)


def draw_headline(draw, xy, text, fill, max_width, start_size, stroke=10):
    x, y = xy
    font = fit_font(draw, text, max_width, start_size, stroke)
    draw.text((x + 8, y + 11), text, font=font, fill=(0, 0, 0, 210), stroke_width=stroke + 3, stroke_fill=(0, 0, 0, 230))
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(8, 8, 8, 255))
    return draw.textbbox((x, y), text, font=font, stroke_width=stroke)[3]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--line1", required=True)
    parser.add_argument("--line2", required=True)
    parser.add_argument("--banner", required=True)
    parser.add_argument("--accent", required=True)
    args = parser.parse_args()

    source = Image.open(args.input).convert("RGB")
    image = ImageOps.fit(source, CANVAS, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5)).convert("RGBA")

    # Darken the text zone while retaining the red motion texture.
    shade = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    sd.rectangle((0, 0, 905, 941), fill=(0, 0, 0, 62))
    shade = shade.filter(ImageFilter.GaussianBlur(22))
    image = Image.alpha_composite(image, shade)

    draw = ImageDraw.Draw(image)
    left, max_width = 68, 790
    y = 92
    y = draw_headline(draw, (left, y), args.line1, (255, 222, 0, 255), max_width, 186, 10) + 4
    y = draw_headline(draw, (left, y), args.line2, (255, 255, 255, 255), max_width, 158, 10) + 30

    banner_font = fit_font(draw, args.banner, max_width - 58, 92, 4)
    banner_box = draw.textbbox((0, 0), args.banner, font=banner_font, stroke_width=4)
    bw = min(max_width, banner_box[2] - banner_box[0] + 64)
    bh = banner_box[3] - banner_box[1] + 38
    draw.rounded_rectangle((left, y, left + bw, y + bh), radius=13, fill=(220, 15, 21, 245), outline=(255, 236, 208, 255), width=3)
    draw.text((left + 31, y + 13), args.banner, font=banner_font, fill=(255, 255, 255, 255), stroke_width=4, stroke_fill=(100, 0, 0, 255))

    # Bottom accent bar makes the design read as a native news thumbnail.
    draw.rounded_rectangle((left, 824, 755, 882), radius=10, fill=(15, 24, 42, 225), outline=(52, 134, 255, 230), width=3)
    small = ImageFont.truetype(FONT, 35)
    draw.text((left + 24, 834), args.accent, font=small, fill=(238, 246, 255, 255))

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(out, "JPEG", quality=94, subsampling=0, optimize=True)


if __name__ == "__main__":
    main()
