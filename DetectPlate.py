from skimage.io import imread
from skimage.filters import threshold_mean


def detect_plate(image_url):
    counter = 0
    car_image = imread(image_url, as_gray=True)
    import matplotlib.pyplot as plt
    gray_car_image = car_image * 255
    # gray_car_image = imutils.rotate(gray_car_image, 350)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(gray_car_image, cmap="gray")
    threshold_value = threshold_mean(gray_car_image)
    binary_car_image = gray_car_image > threshold_value
    # print(binary_car_image)
    ax2.imshow(binary_car_image, cmap="gray")
    plt.savefig(f"output/output_{counter}.png", bbox_inches='tight', pad_inches=0, dpi=200)
    counter = counter + 1

    # ax2.imshow(gray_car_image, cmap="gray")
    # plt.show()

    # CCA (finding connected regions) of binary image

    from skimage import measure
    from skimage.measure import regionprops
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    # this gets all the connected regions and groups them together
    label_image = measure.label(binary_car_image)

    print(label_image.shape)  # width of car img

    # getting the maximum width, height and minimum width and height that a license plate can be
    plate_dimensions = (
        0.01 * label_image.shape[0], 0.08 * label_image.shape[0], 0.1 * label_image.shape[1],
        0.3 * label_image.shape[1])
    plate_dimensions2 = (
        0.08 * label_image.shape[0], 0.99 * label_image.shape[0], 0.15 * label_image.shape[1],
        0.99 * label_image.shape[1])
    min_height, max_height, min_width, max_width = plate_dimensions
    plate_objects_cordinates = []
    plate_like_objects = []

    fig, (ax1) = plt.subplots(1)
    ax1.imshow(binary_car_image, cmap="gray")
    flag = 0
    # regionprops creates a list of properties of all the labelled regions
    for region in regionprops(label_image):
        # print(region)
        if region.area < 50:
            # if the region is so small then it's likely not a license plate
            continue
            # the bounding box coordinates
        min_row, min_col, max_row, max_col = region.bbox
        # print(min_row)
        # print(min_col)
        # print(max_row)
        # print(max_col)

        region_height = max_row - min_row
        region_width = max_col - min_col
        # print(region_height)
        # print(region_width)

        # ensuring that the region identified satisfies the condition of a typical license plate
        if 5 > region_width / region_height > 3 and region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
            flag = 1
            plate_like_objects.append(binary_car_image[min_row:max_row,
                                      min_col:max_col])
            plate_objects_cordinates.append((min_row, min_col,
                                             max_row, max_col))
            rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
                                           linewidth=2, fill=False)
            ax1.add_patch(rectBorder)
            # let's draw a red rectangle over those regions
    if (flag == 1):
        plt.savefig(f"output/output_{counter}.png", bbox_inches='tight', pad_inches=0, dpi=200)
        counter = counter + 1

        # print(plate_like_objects[0])
        #plt.show()

    # if(flag==0):
    min_height, max_height, min_width, max_width = plate_dimensions2
    # plate_objects_cordinates = []
    # plate_like_objects = []

    fig, (ax1) = plt.subplots(1)
    ax1.imshow(gray_car_image, cmap="gray")

    # regionprops creates a list of properties of all the labelled regions
    for region in regionprops(label_image):
        if region.area < 50:
            # if the region is so small then it's likely not a license plate
            continue
            # the bounding box coordinates
        min_row, min_col, max_row, max_col = region.bbox
        # print(min_row)
        # print(min_col)
        # print(max_row)
        # print(max_col)

        region_height = max_row - min_row
        region_width = max_col - min_col
        # print(region_height)
        # print(region_width)

        # ensuring that the region identified satisfies the condition of a typical license plate
        if 5 > region_width / region_height > 3 and region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
            # print("hello")
            plate_like_objects.append(binary_car_image[min_row:max_row,
                                      min_col:max_col])
            plate_objects_cordinates.append((min_row, min_col,
                                             max_row, max_col))
            rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
                                           linewidth=2, fill=False)
            ax1.add_patch(rectBorder)
            # let's draw a red rectangle over those regions
        # print(plate_like_objects[0])
    plt.savefig(f"output/output_{counter}.png", bbox_inches='tight', pad_inches=0, dpi=200)

    # plt.show()
    return plate_like_objects
