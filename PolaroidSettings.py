from enum import Enum


class ImageFactor:
    def __init__(self, left, right, top, bottom, main_text_height, main_text_start, sub_text_height, sub_text_start, main_text_rotation, main_text_font_factor, sub_text_font_factor, main_text_alignment, sub_text_alignment):
        self.left_factor = left
        self.right_factor = right
        self.bottom_factor = bottom
        self.top_factor = top

        self.main_text_height_factor = main_text_height
        self.main_text_start_factor = main_text_start
        self.sub_text_height_factor = sub_text_height
        self.sub_text_start_factor = sub_text_start

        self.main_text_rotation_angle = main_text_rotation
        self.main_text_font_factor = main_text_font_factor
        self.main_text_alignment = main_text_alignment
        self.sub_text_alignment = sub_text_alignment
        self.sub_text_font_factor = sub_text_font_factor



class ImageSettings:
    def __init__(self, landscape_factor, portrait_factor, portrait_blur=False, is_compacted=False):
        self.portrait_factor = portrait_factor
        self.landscape_factor = landscape_factor
        self.requires_blur_for_portrait = portrait_blur
        self.is_compacted = is_compacted

class PolaroidType(Enum):
   FULL_POLAROID = ImageSettings(
       portrait_factor=ImageFactor(0.02,0.02,0.02,0.13,0.93, 0.5, 0.96,0.5, 0,30.44,46.14, "left", "left"),
       landscape_factor=ImageFactor(0.02,0.02,0.02,0.125,0.93, 0.5, 0.965,0.5, 0,29.44,44.14, "left", "left")
   )
   INSTA_SQUARED = ImageSettings(
       portrait_factor=ImageFactor(0,0,0.07,0.13,0.94, 0.5, 0.97,0.5, 0,34.44,48.14, "left", "left"),
       landscape_factor=ImageFactor(0,0,0.07,0.145,0.925, 0.5, 0.96,0.5, 0,30.44,44.14, "left", "left"),
       portrait_blur=True
   )
   HALF_POLAROID = ImageSettings(
       portrait_factor=ImageFactor(0, 0, 0.03, 0.13, 0.93, 0.5, 0.955, 0.5, 0,30.44,44.14, "left", "left"),
       landscape_factor=ImageFactor(0, 0, 0.03, 0.145, 0.91, 0.5, 0.945, 0.5, 0,30.44,44.14, "left", "left")
   )
   QUARTER_POLAROID = ImageSettings(
       portrait_factor=ImageFactor(0, 0, 0, 0.11, 0.945, 0.5, 0.97, 0.5, 0,30.44,44.14, "left", "left"),
       landscape_factor=ImageFactor(0, 0, 0, 0.12, 0.925, 0.5, 0.965, 0.5, 0,30.44,44.14, "left", "left")
   )

   FULL_POLAROID_COMPACT = ImageSettings(
       portrait_factor=ImageFactor(0.02,0.02,0.02,0.13,0.945, 0.05, 0.96,0.95, 0,33.44,48.14, "left", "right"),
       landscape_factor=ImageFactor(0.02,0.02,0.02,0.125,0.94, 0.05, 0.96,0.95, 0,32.44,44.14, "left", "right"),
       is_compacted=True
   )
   INSTA_SQUARED_COMPACT = ImageSettings(
       portrait_factor=ImageFactor(0,0,0.07,0.13,0.96, 0.05, 0.975,0.95, 0,33.44,48.14, "left", "right"),
       landscape_factor=ImageFactor(0,0,0.07,0.145,0.94, 0.05, 0.955,0.95, 0,31.44,44.14, "left", "right"),
       portrait_blur=True,
       is_compacted=True
   )
   HALF_POLAROID_COMPACT = ImageSettings(
       portrait_factor=ImageFactor(0, 0, 0.03, 0.13, 0.945, 0.05, 0.955, 0.95, 0,34.44,48.14, "left", "right"),
       landscape_factor=ImageFactor(0, 0, 0.03, 0.145, 0.935, 0.05, 0.945, 0.95, 0,30.44,44.14, "left", "right"),
       is_compacted=True
   )
   QUARTER_POLAROID_COMPACT = ImageSettings(
       portrait_factor=ImageFactor(0, 0, 0, 0.11, 0.955, 0.05, 0.97, 0.95, 0,33.44,47.14, "left", "right"),
       landscape_factor=ImageFactor(0, 0, 0, 0.12, 0.945, 0.05, 0.96, 0.95, 0,30.44,44.14, "left", "right"),
       is_compacted=True
   )

class ColorSchema:
    def __init__(self, main_line_color, sub_line_color, background_color):
        self.main_color = main_line_color
        self.sub_color = sub_line_color
        self.background_color = background_color

class ColorMode(Enum):
    LIGHT = ColorSchema((0, 0, 0), (128, 128, 128), (255, 255, 255))
    DARK = ColorSchema((255, 255, 255), (128, 128, 128),(0, 0, 0))