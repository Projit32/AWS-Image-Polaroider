import uuid
from uuid import UUID

from PIL import ImageOps, ImageDraw, ImageFont, ImageFile
from PIL import Image
from PIL.ExifTags import TAGS
import PIL
PIL.Image.MAX_IMAGE_PIXELS = 933120000

def add_margin(pil_img:Image.Image, top:int, right:int, bottom:int, left:int, color:tuple) -> Image.Image:
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def draw_text(pil_image: Image.Image, message: str, font_color: tuple, width_factor: float,height_factor: float, font: str, font_size: int) -> Image.Image:
    W, H = pil_image.size
    draw = ImageDraw.Draw(pil_image)
    font = ImageFont.truetype(font, font_size)
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((W-w)*width_factor, (H-h)*height_factor), message, font=font, fill=font_color)
    return pil_image


def generate_polaroid(image_URL:str) -> Image.Image:
    with Image.open(image_URL) as im:

        width = im.width
        height = im.height
        context_size = height if height > width else width

        polaroid_image = add_margin(ImageOps.exif_transpose(im), int(context_size * 0.02), int(context_size * 0.02),
                                    int(context_size * 0.15), int(context_size * 0.02), (255, 255, 255))

        exif_data = im._getexif()
        metadata_keys = ["Make", "Model", "DateTime", "ImageWidth", "ImageLength", "FocalLength", "MaxApertureValue",
                         "ISOSpeedRatings", "ShutterSpeedValue"]
        metadata_dict = dict()
        # iterating over all EXIF data fields
        for tag_id in exif_data:
            # get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            data = exif_data.get(tag_id)
            # decode bytes
            if isinstance(data, bytes):
                data = data.decode()
            if tag in metadata_keys:
                metadata_dict[tag] = str(data)

        print(metadata_dict)

        main_line = ""

        if metadata_dict.get("Make") and metadata_dict.get("Model"):
            main_line = (metadata_dict.get("Make") + " " + metadata_dict.get("Model")).title()

        if metadata_dict.get("DateTime"):
            if main_line:
                main_line += "   |   " + metadata_dict.get("DateTime")
            else:
                main_line = metadata_dict.get("DateTime")

        print("Main line :", main_line)

        polaroid_image = draw_text(polaroid_image, main_line, (0, 0, 0), 0.5, 0.9,
                                   "./fonts/lato.heavy.ttf", 90)

        sub_line = metadata_dict.get("ImageWidth") + "x" + metadata_dict.get("ImageLength")

        if metadata_dict.get("MaxApertureValue"):
            sub_line += "   f/" + metadata_dict.get("MaxApertureValue")

        if metadata_dict.get("ShutterSpeedValue"):
            sub_line += "   1/" + str(1 / float(metadata_dict.get("ShutterSpeedValue")))

        if metadata_dict.get("FocalLength"):
            sub_line += "   " + metadata_dict.get("FocalLength") + "mm"

        if metadata_dict.get("ISOSpeedRatings"):
            sub_line += "   ISO" + metadata_dict.get("ISOSpeedRatings")

        print("Sub line :", sub_line)
        polaroid_image = draw_text(polaroid_image, sub_line, (128, 128, 128), 0.5, 0.95,
                                   "./fonts/lato.light-italic.ttf", 70)

        return polaroid_image

if __name__ == "__main__":
        generate_polaroid("E:\\photos\\20240112_164420.jpg").save("./output/"+str(uuid.uuid4())+".png")







