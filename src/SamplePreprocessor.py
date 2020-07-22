from __future__ import division
from __future__ import print_function

import random
import numpy as np
import cv2

def preprocess(img, imgSize, dataAugmentation=False):
    "put img into target img of size imgSize, transpose for tensorflow and normalize gray-values"

    # There are damaged files in IAM dataset - just use black image instead
    if img is None:
        img = np.zeros([imgSize[1], imgSize[0]])

    #  Increase dataset size by applying random stretches to the images
    if dataAugmentation:
        stretch = (random.random() - 0.5)
        wStretched = max(int(img.shape[1] * (1 + stretch)), 1)
        img = cv2.resize(img, (wStretched, img.shape[0]))

    # creating target image and copy sample image into it
    (wt, ht) = imgSize
    (h, w) = img.shape
    fx = w / wt
    fy = h / ht
    f = max(fx, fy)
    newSize = (max(min(wt, int(w / f)), 1), max(min(ht, int(h / f)), 1))
    img = cv2.resize(img, newSize)
    target = np.ones([ht, wt]) * 255
    target[0:newSize[1], 0:newSize[0]] = img

    # transpose for Tensorflow
    img = cv2.transpose(target)

    # normalize
    (m, s) = cv2.meanStdDev(img)
    m = m[0][0]
    s = s[0][0]
    img = img - m
    img = img / s if s>0 else img
    return img