import concurrent.futures
import os
import traceback
import uuid

from PolaroidBuilder import generate_polaroid
from PolaroidSettings import ColorMode, PolaroidMode

import resource
resource.setrlimit(resource.RLIMIT_AS, (1000000000,1000000000))

error_items = list()


def main(data):
    try:
        generate_polaroid(data["image"], data["type"], data["color"]).save("./output/" + str(uuid.uuid4()) + ".png",
                                                                           "PNG",
                                                                           compress_level=1)
    except Exception as e:
        traceback.print_exc()
        print("Exception", str(e))
        error_items.append(data)

    return error_items


if __name__ == "__main__":

    values = ["./input/" + item for item in os.listdir("./input")]
    print("Initial Input Size", len(values))

    data = []

    print("Preparing data")
    for image in values:
        data.append({"image": image, "color": ColorMode.DARK, "type": PolaroidMode.INSTA_SQUARED_COMPACT})


    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as exe:
        exe.map(main, data)

    print("final error Size", len(error_items), error_items)