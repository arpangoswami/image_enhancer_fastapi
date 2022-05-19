import pywt
import cv2 as cv
import numpy as np
import base64
import uuid


def data_uri_to_cv2_img(uri: str):
    encoded_data = uri.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)
    blurred_image_name = str(uuid.uuid4())
    blurred_image_name += ".jpg"
    return img


# This function does the coefficient fusing according to the fusion method
def fuseCoeff(cooef1, cooef2, method):
    if method == 'mean':
        cooef = (cooef1 + cooef2) / 2
    elif method == 'min':
        cooef = np.minimum(cooef1, cooef2)
    elif method == 'max':
        cooef = np.maximum(cooef1, cooef2)
    else:
        cooef = []
    return cooef


# Params
FUSION_METHOD = 'mean'  # Can be 'min' || 'max || anything you choose according theory


def wavelet_fusion(blur, grayscale):
    grayscale = cv.resize(grayscale, (blur.shape[1], blur.shape[0]))
    # Fusion algo
    # First: Do wavelet transform on each image
    wavelet = 'db1'
    cooef1 = pywt.wavedec2(blur[:, :], wavelet)
    cooef2 = pywt.wavedec2(grayscale[:, :], wavelet)
    # Second: for each level in both image do the fusion according to the desire option
    fused_coeff = []
    for i in range(len(cooef1) - 1):

        # The first values in each decomposition is the apprximation values of the top level
        if i == 0:

            fused_coeff.append(fuseCoeff(cooef1[0], cooef2[0], FUSION_METHOD))

        else:
            # For the rest of the levels we have tupels with 3 coeeficents
            c1 = fuseCoeff(cooef1[i][0], cooef2[i][0], FUSION_METHOD)
            c2 = fuseCoeff(cooef1[i][1], cooef2[i][1], FUSION_METHOD)
            c3 = fuseCoeff(cooef1[i][2], cooef2[i][2], FUSION_METHOD)

            fused_coeff.append((c1, c2, c3))

    # Third: After we fused the co-efficient we need to transfer back to get the image
    fused_image = pywt.waverec2(fused_coeff, wavelet)

    # Forth: normalize values to be in uint8
    fused_image = np.multiply(np.divide(
        fused_image - np.min(fused_image), (np.max(fused_image) - np.min(fused_image))), 255)
    fused_image = fused_image.astype(np.uint8)
    return fused_image


def get_fused_image(uri1: str, uri2: str) -> str:
    grayscale_image = data_uri_to_cv2_img(uri1)
    blurred_image = data_uri_to_cv2_img(uri2)

    (blueBlur, greenBlur, redBlur) = cv.split(blurred_image)
    (blueGrayscaleBlur, greenGrayscaleBlur, redGrayscaleBlur) = cv.split(grayscale_image)

    blueFused = wavelet_fusion(blueBlur, blueGrayscaleBlur)
    greenFused = wavelet_fusion(greenBlur, greenGrayscaleBlur)
    redFused = wavelet_fusion(redBlur, redGrayscaleBlur)

    fusedImage = cv.merge([blueFused, greenFused, redFused])

    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    image_sharp = cv.filter2D(src=fusedImage, ddepth=-1, kernel=kernel)
    resized_sharpened = cv.resize(
        image_sharp, (blurred_image.shape[1], blurred_image.shape[0]))

    # line that fixed it
    _, encoded_img = cv.imencode('.JPEG', resized_sharpened)

    encoded_img_jpeg = "data:image/jpeg;base64,"
    encoded_img_jpeg += base64.b64encode(encoded_img).decode('utf-8')

    return encoded_img_jpeg
