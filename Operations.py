# -*- coding: utf-8 -*-
# region IMPORTED LIBRARIES

# endregion

# region GLOBAL VARIABLES
imagePath = ''
img = np.zeros(0)
cvImg = np.zeros(0)
opImg = np.zeros(0)
panel = []
undoList = list()
redoList = list()
# endregion

# region DISPLAY IMAGE ON FRAME FUNCTION

# endregion

# region UNDO/REDO IMAGE FUNCTIONS

# endregion

# region SAVING IMAGE FILE AS PNG FUNCTIONS

# endregion

# region LOCAL RESET AND SAVE FUNCTIONS

# endregion

# region RESIZE IMAGE FOR DYNAMIC FRAME

# endregion

# region LOAD IMAGE FUNCTION

# endregion

# region GRAYSACLE FUNCTION

# endregion

# region MIRROR FUNCTION

# endregion

# region CROP FUNCTION


# operation : left,right,top,bottom,horizantal(left-right), vertical(top-bottom),all

# endregion

# region BRIGHTNESS & DARKNESS FUNCTION

# endregion

# region CONTRAST FUNCTION

# endregion

# region BLUR FUNCTION

# endregion

# region DEBLUR FUNCTION (NOT WORKING CORRECTLY)

# endregion

# region INVERT FUNCTION

# endregion

# region HISTOGRAM NORMALIZATION FUNCTION

# endregion

# region MORPHOLOGICAL TRANSFORMATION FUNCTION

# endregion

# region COLOR CHANNELS FUNCTION

# endregion

# region RESIZE IMAGE FUNCTION

# endregion

# region AUTOMATIC BRIGHTNESS AND CONTRAST FUNCTION

# endregion

# region downsideUpFilter FUNCTION


def downsideUpFilter():
    global opImg
    global img

    kernel = np.array([[1, -1, 0], [-1, 4, -1], [-1, 0, -1]])
    # applying the kernel to the input image
    opImg = cv2.filter2D(img, -1, kernel)
    DisplayImage(opImg)
    pass
# endregion

# region SoftBWfilter FUNCTION


def SoftBWfilter():
    global opImg
    global img

    # allow the filter to process 30 times
    count = 30
    for _ in range(count):
        # smoothening images and reducing noise
        img_color = cv2.bilateralFilter(img, 10, 7, 3)
    opImg = cv2.cvtColor(img_color, cv2.COLOR_RGB2GRAY)
    DisplayImage(opImg)
    pass
# endregion

# region cartoonizerEffectFilter FUNCTION


def cartoonizerEffectFilter():
    global opImg
    global img

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # bluring
    gray = cv2.medianBlur(gray, 3)
    # edges were exposed
    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 11)
    # smoothening images and reducing noise
    color = cv2.bilateralFilter(img, 9, 100, 100)
    # combining edges and color images
    opImg = cv2.bitwise_and(color, color, mask=edges)
    opImg = cv2.cvtColor(opImg, cv2.COLOR_BGR2RGB)

    DisplayImage(opImg)
    pass
# endregion

# region asheFilter FUNCTION


def asheFilter():
    global opImg
    global img

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # bluring
    gray_blur = cv2.GaussianBlur(gray, (25, 25), 200)
    # divide blured image and gray image
    opImg = cv2.divide(gray, gray_blur, scale=100.0)
    DisplayImage(opImg)


    pass
# endregion

# region BRossFilter FUNCTION


def BRossFilter():
    global opImg
    global img

    # smoothening images and reducing noise
    img = cv2.bilateralFilter(img, 9, 100, 100)
    # changing the color channel in a different way
    b, g, r = cv2.split(img)
    opImg = cv2.merge((r, g, b))
    DisplayImage(opImg)


    pass
# endregion

# region NegativeFilter FUNCTION


def negativeFilter():
    global opImg
    global img

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # collapsed into one dimension
    k = img_gray.flatten()
    L = max(k)  # getting max value

    for i in range(img_gray.shape[0]):
        for j in range(img_gray.shape[1]):
            # getting reverse version of gray image
            img_gray[i, j] = L - img_gray[i, j]
    opImg = img_gray
    DisplayImage(opImg)


    pass
# endregion

# region coolFilter FUNCTION


def LUT_func(x, y):
    # Reduced to a single dimension
    spl = UnivariateSpline(x, y)
    return spl(range(256))


def coolFilter():
    global opImg
    global img

    incLUT = LUT_func([0, 64, 128, 192, 256], [0, 70, 140, 210, 256])
    decLUT = LUT_func([0, 64, 128, 192, 256], [0, 30, 80, 120, 192])

    c_b, c_g, c_r = cv2.split(img)
    # colormap that stored in a 256 x 1 color image  applied to an image using a lookup table LUT
    c_b = cv2.LUT(c_b, incLUT).astype(np.uint8)
    c_r = cv2.LUT(c_r, decLUT).astype(np.uint8)
    # decreasing the red color channel revealing the blue color channel
    img_rgb = cv2.merge((c_r, c_g, c_b))
    # Saturation was reduced to make these colors brighter than normal blue perception
    c_h, c_s, c_v = cv2.split(cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV))
    c_s = cv2.LUT(c_s, decLUT).astype(np.uint8)
    img_hsv = cv2.merge((c_h, c_s, c_v))
    opImg = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)
    DisplayImage(opImg)


    pass
# endregion

# region carbonPaperFilter FUNCTION


def carbonPaperFilter():
    global opImg
    global img

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # To obtain clear image in threshold
    img_blur = cv2.medianBlur(img_gray, 3)
    # edges were exposed
    opImg = cv2.adaptiveThreshold(
        img_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 7)

    DisplayImage(opImg)


    pass
# endregion

# region warmFilter FUNCTION


def warmFilter():
    global opImg
    global img

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    increaseLUT = LUT_func([0, 64, 128, 192, 256], [0, 70, 140, 210, 256])
    decreaseLUT = LUT_func([0, 64, 128, 192, 256], [0, 30, 80, 120, 192])
    # colormap that stored in a 256 x 1 color image  applied to an image using a lookup table LUT
    c_r, c_g, c_b = cv2.split(img)
    # decreasing the blue color channel increasing the red color channel
    c_r = cv2.LUT(c_r, increaseLUT).astype(np.uint8)
    c_b = cv2.LUT(c_b, decreaseLUT).astype(np.uint8)
    img_rgb = cv2.merge((c_r, c_g, c_b))
    c_h, c_s, c_v = cv2.split(cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV))
    # Saturation was reduced to make these colors brighter than normal blue perception
    c_s = cv2.LUT(c_s, decreaseLUT).astype(np.uint8)
    img_hsv = cv2.merge((c_h, c_s, c_v))
    opImg = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)
    DisplayImage(opImg)

    pass
# endregion

# region masterSketcherFilter FUNCTION

def dodge_img(x,y):
    return cv2.divide(x,255-y,scale=256)
def burn_img(image, mask):
    return 255 - cv2.divide(255-image, 255-mask, scale=256)

def change_brightness(image, value=30):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v,value)
    v[v > 255] = 255
    v[v < 0] = 0
    final = cv2.merge((h, s, v))
    image = cv2.cvtColor(final, cv2.COLOR_HSV2BGR)
    return image

def masterSketcherFilter():
    global opImg
    global img

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # intensity 0
    img_bit = cv2.bitwise_not(gray)
    # bluring
    img_blur = cv2.GaussianBlur(img_bit, (21, 21), sigmaX=0, sigmaY=0)
    # converts the image to a faded image
    img_d = dodge_img(gray, img_blur)
    # image getting more dark
    final = burn_img(img_d, img_blur)
    # change brightness convert BGR then convert Gray
    gray = cv2.cvtColor(final, cv2.COLOR_GRAY2BGR)
    # result approaches the drawing view, the image is dimmed
    final = change_brightness(gray, value=-10)
    opImg = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)

    DisplayImage(opImg)
    pass
# endregion

# region coloredMasterSketcherFilter FUNCTION
def change_saturation(image, value=30):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = cv2.add(s,value)
    s[s > 255] = 255
    s[s < 0] = 0
    final = cv2.merge((h, s, v))
    image = cv2.cvtColor(final, cv2.COLOR_HSV2BGR)
    return image

def coloredMasterSketcherFilter():
    global opImg
    global img

    # vivid colors in the final image are rendered realistic
    image = change_saturation(img, value=-40)
    img_bit = cv2.bitwise_not(image)
    img_blur = cv2.GaussianBlur(img_bit, (21, 21), sigmaX=0, sigmaY=0)
    img_d = dodge_img(image, img_blur)
    final = burn_img(img_d, img_blur)
    opImg = change_brightness(final, value=-5)
    DisplayImage(opImg)

    pass
# endregion

# region embossFilter FUNCTION


def embossFilter():
    global opImg
    global img

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # emboss filter
    kernel = np.array(([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]]), np.float32)
    # filter applied
    opImg = cv2.filter2D(src=img, kernel=kernel, ddepth=-2)
    DisplayImage(opImg)
    pass
# endregion

# region DownsideNeonFilter FUNCTION


def downsideNeonFilter():
    global opImg
    global img

    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    # applying the kernel to the input image
    kernel = np.array(
        ([[0, -1, 0], [-1, 4, -1], [0, -1, 0]]), np.float32)
    filter = cv2.filter2D(src=img, kernel=kernel, ddepth=-1)
    # applying the kernel2 to the input filtered image it makes the image sharper and neon colored
    kernel2 = np.array(
        ([[0, 2, 0], [-2, 5, -1], [0, -1, 0]]), np.float32)
    opImg = cv2.filter2D(src=filter, kernel=kernel2, ddepth=-5)
    DisplayImage(opImg)


    pass
# endregion


# region markedFilter FUNCTION


def markedFilter():
    global opImg
    global img

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # inverse version of color chanel
    img_bit = cv2.bitwise_not(img)
    # bluring
    blured = cv2.GaussianBlur(img_bit, (17, 53), sigmaX=8, sigmaY=10)
    # divide blured img and blured image but inverse version of blured image
    opImg = cv2.divide(img, 255 - blured, scale=256)
    DisplayImage(opImg)


    pass
# endregion
