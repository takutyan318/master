#! /usr/bin/env python
# coding: utf-8

#いろいろなテスト用

import cv2
import numpy as np
import sys


img = cv2.imread('../image/face/test_front.jpeg')
print img.shape[0], img.shape[1]