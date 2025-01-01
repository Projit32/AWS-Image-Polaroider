from enum import Enum


class ImageFactor:
    def __init__(self, left, right, top, bottom, main_text_height, main_text_start, sub_text_height, sub_text_start, main_text_rotation):
        self.left_factor = left
        self.right_factor = right
        self.bottom_factor = bottom
        self.top_factor = top

        self.main_text_height_factor = main_text_height
        self.main_text_start_factor = main_text_start
        self.sub_text_height_factor = sub_text_height
        self.sub_text_start_factor = sub_text_start

        self.main_text_rotation_angle = main_text_rotation



class ImageMode:
    def __init__(self, landscape_factor, portrait_factor, portrait_blur=False):
        self.portrait_factor = portrait_factor
        self.landscape_factor = landscape_factor
        self.requires_blur_for_portrait =portrait_blur

class PolaroidType(Enum):
   FULL_POLAROID = ImageMode(
       portrait_factor=ImageFactor(0.02,0.02,0.02,0.13,0.93, 0.5, 0.955,0.5, 0),
       landscape_factor=ImageFactor(0.02,0.02,0.02,0.145,0.9, 0.5, 0.94,0.5, 0)
   )
   INSTA_SQUARED = ImageMode(
       portrait_factor=ImageFactor(0,0,0.07,0.13,0.93, 0.5, 0.955,0.5, 0),
       landscape_factor=ImageFactor(0,0,0.07,0.145,0.93, 0.5, 0.96,0.5, 0),
       portrait_blur=True
   )
   HALF_POLAROID = ImageMode(
       portrait_factor=ImageFactor(0, 0, 0.03, 0.13, 0.93, 0.5, 0.955, 0.5, 0),
       landscape_factor=ImageFactor(0, 0, 0.03, 0.145, 0.9, 0.5, 0.94, 0.5, 0)
   )
   QUARTER_POLAROID = ImageMode(
       portrait_factor=ImageFactor(0, 0, 0, 0.13, 0.93, 0.5, 0.955, 0.5, 0),
       landscape_factor=ImageFactor(0, 0, 0, 0.145, 0.9, 0.5, 0.94, 0.5, 0)
   )