from PIL import ImageOps, ImageDraw
from PIL import Image
from PIL.ExifTags import TAGS
import PIL
PIL.Image.MAX_IMAGE_PIXELS = 933120000



def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

if __name__ == "__main__":
    with Image.open("") as im:

        width = im.width
        height = im.height
        context_height = height if height > width else width

        polaroid_image = add_margin(ImageOps.exif_transpose(im), int(context_height*0.02), int(context_height*0.02), int(context_height*0.15), int(context_height*0.02), (255, 255, 255))

        exifdata = im._getexif()
        metadata_keys = ["ImageWidth", "ImageLength", "Make", "Model", "DateTime", "FocalLength", "MaxApertureValue", "ISOSpeedRatings", "ShutterSpeedValue"]
        metadata_dict = dict()
        # iterating over all EXIF data fields
        for tag_id in exifdata:
            # get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            # decode bytes
            if isinstance(data, bytes):
                data = data.decode()
            if tag in metadata_keys:
                metadata_dict[tag] = data

        print(metadata_dict)

        ImageDraw.Draw(
            polaroid_image  # Image
        ).text(
            (0, 0),  # Coordinates
            'Hello world!',  # Text
            (0, 0, 0)  # Color
        )