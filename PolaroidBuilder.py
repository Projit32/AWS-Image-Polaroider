from io import BytesIO
from PolaroidSettings import PolaroidMode, ImageFactor, ColorMode
from datetime import datetime
from PIL import ImageOps, ImageDraw, ImageFont, ImageFilter
from PIL import Image
from PIL.ExifTags import TAGS
import PIL
from memory_profiler import profile
from PIL.TiffImagePlugin import IFDRational
PIL.Image.MAX_IMAGE_PIXELS = 933120000

@profile
def add_margin(pil_img:Image.Image, top:int, right:int, bottom:int, left:int, color:tuple) -> Image.Image:
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

@profile
def draw_text(pil_image: Image.Image, message: str, font_color: tuple, width_factor: float,height_factor: float, font: str, font_size: int, alignment:str = "left") -> Image.Image:
    W, H = pil_image.size
    draw = ImageDraw.Draw(pil_image)
    font = ImageFont.truetype(font, font_size)
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((W-w)*width_factor, (H-h)*height_factor), message, font=font, fill=font_color, align=alignment)
    return pil_image

@profile
def get_meta_data(im: Image) -> dict:
    exif_data = im._getexif()
    metadata_keys = ["Make", "Model", "DateTime", "ImageWidth", "ImageLength", "FocalLength", "MaxApertureValue",
                     "ISOSpeedRatings", "ExposureTime"]
    metadata_dict = dict()
    # iterating over all EXIF data fields
    if exif_data:
        for tag_id in exif_data:
            # get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            data = exif_data.get(tag_id)
            if tag in metadata_keys and str(data) != "nan":
                # decode bytes
                if isinstance(data, bytes):
                    data = data.decode()
                metadata_dict[tag] = str(data)

    return metadata_dict

@profile
def generate_standard_text_lines(metadata_dict:dict, width:float, height:float):
    main_line = ""

    if metadata_dict.get("Make") and metadata_dict.get("Model"):
        main_line = (metadata_dict.get("Make") + " " + metadata_dict.get("Model")).title()

    if metadata_dict.get("DateTime"):
        if main_line:
            main_line += "    [ " + datetime.strptime(metadata_dict.get("DateTime"), "%Y:%m:%d %H:%M:%S").strftime("%a,  %d-%b-%Y  %H:%M:%S")+" ]"
        else:
            main_line = metadata_dict.get("DateTime")

    print("Main line :", main_line)

    sub_line = "{0:.1f}".format((height * width) / 1000000) + "MP"
    if metadata_dict.get("ImageWidth") and metadata_dict.get("ImageLength"):
        sub_line += "   " + metadata_dict.get("ImageWidth") + "x" + metadata_dict.get("ImageLength")
    else:
        sub_line += "   " + str(width) + "x" + str(height)

    if metadata_dict.get("MaxApertureValue"):
        sub_line += "   f/" + metadata_dict.get("MaxApertureValue")

    if metadata_dict.get("ExposureTime"):
        sub_line += "   1/" + str(int(1 / float(metadata_dict.get("ExposureTime")))) + "s"

    if metadata_dict.get("FocalLength"):
        sub_line += "   " + metadata_dict.get("FocalLength") + "mm"

    if metadata_dict.get("ISOSpeedRatings"):
        sub_line += "   ISO" + metadata_dict.get("ISOSpeedRatings")

    print("Sub line :", sub_line)

    return main_line, sub_line

@profile
def generate_compacted_text_lines(metadata_dict:dict, width:float, height:float):
    main_line = ""

    if metadata_dict.get("Make") and metadata_dict.get("Model"):
        main_line = (metadata_dict.get("Make") + " " + metadata_dict.get("Model")).title()

    print("Main line :", main_line)

    sub_line = "{0:.1f}".format((height * width) / 1000000) + "MP"
    if metadata_dict.get("ImageWidth") and metadata_dict.get("ImageLength"):
        sub_line += "   " + metadata_dict.get("ImageWidth") + "x" + metadata_dict.get("ImageLength")
    else:
        sub_line += "   " + str(width) + "x" + str(height)

    if metadata_dict.get("MaxApertureValue"):
        sub_line += "   f/" + metadata_dict.get("MaxApertureValue")

    if metadata_dict.get("ExposureTime"):
        sub_line += "   1/" + str(int(1 / float(metadata_dict.get("ExposureTime")))) + "s"

    if metadata_dict.get("FocalLength"):
        sub_line += "   " + metadata_dict.get("FocalLength") + "mm"

    if metadata_dict.get("ISOSpeedRatings"):
        sub_line += "   ISO" + metadata_dict.get("ISOSpeedRatings")

    if metadata_dict.get("DateTime"):
        date = datetime.strptime(metadata_dict.get("DateTime"), "%Y:%m:%d %H:%M:%S").strftime("%c")
        sub_line += "\n\n"+date
    else:
        sub_line += "\n‎ "

    print("Sub line :", sub_line)

    return main_line, sub_line

@profile
def blur_burst_center_image(im:Image.Image) -> Image.Image:
    blurred_image = im.filter(ImageFilter.GaussianBlur(200))
    blurred_burst_image = blurred_image.resize((2*im.height, im.height))
    blurred_burst_cropped_image = blurred_burst_image.crop((im.height*0.4, 0, im.height*1.6, im.height))
    left_start = (blurred_burst_cropped_image.width-im.width)//2
    blurred_burst_cropped_image.paste(im, (left_start, 0))
    return blurred_burst_cropped_image


@profile
def generate_polaroid(image_URL:str, polaroid_type:PolaroidMode, color_mode:ColorMode) -> Image.Image:
    with Image.open(image_URL) as im:

        context_size = max(im.height, im.width)
        image = ImageOps.exif_transpose(im)
        print(image.size)
        is_portrait = image.height > image.width

        if polaroid_type.value.requires_blur_for_portrait and is_portrait:
            print("Portrait blur image")
            image = blur_burst_center_image(image)

        image_factor:ImageFactor = polaroid_type.value.landscape_factor if not is_portrait else polaroid_type.value.portrait_factor


        polaroid_image = add_margin(image, int(context_size * image_factor.top_factor), int(context_size * image_factor.left_factor),
                                    int(context_size * image_factor.bottom_factor), int(context_size * image_factor.right_factor), color_mode.value.background_color)

        context_font_size = min(polaroid_image.height, polaroid_image.width)

        main_line, sub_line = generate_compacted_text_lines(get_meta_data(im), im.width, im.height) if polaroid_type.value.is_compacted else generate_standard_text_lines(get_meta_data(im), im.width, im.height)

        polaroid_image = draw_text(polaroid_image, main_line.strip(), color_mode.value.main_color, image_factor.main_text_start_factor, image_factor.main_text_height_factor,
                                   "./fonts/SamsungOne-700.ttf", int(context_font_size / image_factor.main_text_font_factor), image_factor.main_text_alignment)

        polaroid_image = draw_text(polaroid_image, sub_line.strip(), color_mode.value.sub_color, image_factor.sub_text_start_factor, image_factor.sub_text_height_factor,
                                   "./fonts/SamsungOne-400.ttf", int(context_font_size / image_factor.sub_text_font_factor), image_factor.sub_text_alignment)


        return polaroid_image











