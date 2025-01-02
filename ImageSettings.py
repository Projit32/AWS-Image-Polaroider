from enum import Enum


class ImageFactor:
    def __init__(self, left, right, top, bottom, main_text_height, main_text_start, sub_text_height, sub_text_start, main_text_rotation, main_text_font_factor, sub_text_font_factor):
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
        self.sub_text_font_factor = sub_text_font_factor



class ImageMode:
    def __init__(self, landscape_factor, portrait_factor, portrait_blur=False):
        self.portrait_factor = portrait_factor
        self.landscape_factor = landscape_factor
        self.requires_blur_for_portrait =portrait_blur

class PolaroidType(Enum):
   FULL_POLAROID = ImageMode(
       portrait_factor=ImageFactor(0.02,0.02,0.02,0.13,0.93, 0.5, 0.96,0.5, 0,30.44,46.14),
       landscape_factor=ImageFactor(0.02,0.02,0.02,0.125,0.93, 0.5, 0.965,0.5, 0,29.44,44.14)
   )
   INSTA_SQUARED = ImageMode(
       portrait_factor=ImageFactor(0,0,0.07,0.13,0.94, 0.5, 0.97,0.5, 0,34.44,48.14),
       landscape_factor=ImageFactor(0,0,0.07,0.145,0.925, 0.5, 0.96,0.5, 0,30.44,44.14),
       portrait_blur=True
   )
   HALF_POLAROID = ImageMode(
       portrait_factor=ImageFactor(0, 0, 0.03, 0.13, 0.93, 0.5, 0.955, 0.5, 0,30.44,44.14),
       landscape_factor=ImageFactor(0, 0, 0.03, 0.145, 0.91, 0.5, 0.945, 0.5, 0,30.44,44.14)
   )
   QUARTER_POLAROID = ImageMode(
       portrait_factor=ImageFactor(0, 0, 0, 0.11, 0.945, 0.5, 0.97, 0.5, 0,30.44,44.14),
       landscape_factor=ImageFactor(0, 0, 0, 0.12, 0.925, 0.5, 0.965, 0.5, 0,30.44,44.14)
   )