import os

import numpy as np
from skimage.transform import resize
from skimage import measure
# from skimage.measure import regionprops
import matplotlib.patches as patches
import matplotlib.pyplot as plt

import DetectPlate


def segment_characters(image_url):
    characters_array = []
    column_list_array = []
    possible_final_images = []
    for lp in DetectPlate.detect_plate(image_url):
        license_plate = np.invert(lp)

        labelled_plate = measure.label(license_plate)

        fig, ax1 = plt.subplots(1)
        ax1.imshow(license_plate, cmap="gray")
        possible_final_images.append(license_plate)
        character_dimensions = (0.35 * license_plate.shape[0], 0.80 * license_plate.shape[0], 0.05 * license_plate.shape[1],
                                0.25 * license_plate.shape[1])
        min_height, max_height, min_width, max_width = character_dimensions

        possible_characters = []
        possible_column_list = []
        for regions in measure.regionprops(labelled_plate):
            y0, x0, y1, x1 = regions.bbox
            region_height = y1 - y0
            region_width = x1 - x0

            if min_height < region_height < max_height and min_width < region_width < max_width:
                roi = license_plate[y0:y1, x0:x1]

                # draw a red bordered rectangle over the character.
                rect_border = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="red",
                                                linewidth=2, fill=False)
                ax1.add_patch(rect_border)
                # resize the characters to 20X20 and then append each character into the characters list
                resized_char = resize(roi, (20, 20))
                possible_characters.append(resized_char)

                # this is just to keep track of the arrangement of the characters
                possible_column_list.append(x0)


        column_list_array.append(possible_column_list)
        characters_array.append(possible_characters)

    characters_length_array = []
    for c in characters_array:
        characters_length_array.append(len(c))

    temp = np.argsort(characters_length_array)
    wanted_image_index = temp[-1]
    characters_array.sort(key=lambda x: len(x))

    ax1.imshow(possible_final_images[wanted_image_index],  cmap="gray")
    images = next(os.walk('output'))[2]
    plt.savefig(f"output/output_{len(images)}.png", bbox_inches='tight', pad_inches=0, dpi=200)
    # plt.show()
    column_list_array.sort(key=lambda x: len(x))
    characters = characters_array[-1]
    column_list = column_list_array[-1]
    return characters, column_list
