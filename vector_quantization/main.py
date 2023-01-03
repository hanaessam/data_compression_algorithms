import math
from PIL import Image
import numpy as np
import cv2
import os
import sys

np.seterr(over='ignore')

# INPUT/OUTPUT
inputFile = "" #here goes the absolute path of the image you want to compress
outputFile = "" #the absolute path of compressed image

# Read image using OpenCv
src = cv2.imread(sys.path[0] + "/test.jpg", 1)

src = cv2.imread(inputFile, cv2.IMREAD_GRAYSCALE)

cv2.imshow('Input Image', src)
cv2.waitKey(0)  # waits until a key is pressed
cv2.destroyAllWindows()  # destroys the window showing image

# Reading Image using Pillow
img = Image.open(inputFile)
print("Image format: ", img.format)
width, height = img.size
print("Original Image Size: ", os.path.getsize(inputFile), "Bytes")

numpydata = np.array(src) 
res = numpydata.flatten()  # 2D array to 1D array

li = res  # li contains the pixel of the Original Image

# Saving Original Image Pixel in text file
with open('PixelOfOriginalImage.txt', 'w+') as file:
    for l in li:
        file.write("%i " % l)


rang = max(li) - min(li)
pp = math.ceil(rang / 10)
print("Enter the vector size, which should be greater than equal to ", pp)
u = int(input("Enter the vector: "))
interval = math.ceil(rang / u)
mid = round((interval / 2), 2)
print("Interval: ", interval)
print("Midpoint: ", mid)
print(" ")

key = 1  # Implmentation of codebook
codebook = dict()
while key < ((u * u) + 1):
    a = mid
    for v1 in range(1, u + 1, 1):
        b = mid
        for v2 in range(1, u + 1, 1):
            temp = [a, b]
            codebook.update({key: temp})
            key = key + 1
            b = b + interval
        a = a + interval
# print(codebook)

main = []  # main is list
temp = []  # temporary list
for i in range(0, (len(li)), 2):
    for j in range(2, (u * 2 + 1), 2):
        if li[i] <= j * mid:
            break

    for k in range(2, (u * 2 + 1), 2):
        if li[i + 1] <= k * mid:
            break
    temp = [j // 2, k // 2]  # floor value
    main.append(temp)
main = np.asarray(main)  # main is Converted from 'list' to 'array'


quantizeData = []
for i in range(len(main)):
    x = (main[i][0] - 1) * u + main[i][1]  # [3,2]-> (3-1)*u+2
    quantizeData.append(x)
quantizeData = np.array(quantizeData)


# Saving QuantizedData in text file
with open('PixelOFQuantizeData.txt', 'w+') as file:
    for qD in quantizeData:
        file.write("%i " % qD)


midCentroid1 = []
midCentroid2 = []

for i in range(0, len(quantizeData), 1):
    key = quantizeData[i]
    if key in codebook:
        midCentroid1 = [codebook[key]]
        midCentroid2.extend(midCentroid1)

midCentroid2 = np.array(midCentroid2)

arrCen = midCentroid2.flatten()  # In 1D Numpy Array
arrCen2 = np.ceil(np.array(arrCen)).astype(np.uint8)

# Saving Regenrated Image Pixel in Text File
with open('PixelOfRegenatedImage.txt', 'w+') as file:
    for aC in arrCen2:
        file.write("%i " % aC)

newarray = arrCen2.reshape(height, width)  # 1D to 2D Numpy Array

src2 = Image.fromarray(newarray)  # Converting from numpyArray to pillowImage
src2.save(outputFile)  # Saving OutputImage
print('Image is successfully saved as file.')
print("Re Contructed Image Size: ", os.path.getsize(outputFile), "Bytes")  # path of OutputImage File

s = cv2.imread(outputFile, cv2.IMREAD_GRAYSCALE)  # reads newly created compressed image
cv2.imshow('Output Image', s)
cv2.waitKey(0)  # waits until a key is pressed
cv2.destroyAllWindows()  # destroys the window showing image

error = []
for i in range(0, len(li), 2):
    s4 = (pow((li[i] - arrCen2[i]), 2) + (pow((li[i + 1] - arrCen2[i + 1]), 2)))  # Using Distance Formula
    s3 = math.sqrt(s4)
    error.append(s3)
error = np.asarray(error)
print(" ")

correlation_coefficient = np.corrcoef(li, arrCen)
correlation_coefficient1 = np.mean(correlation_coefficient)
print(" Correlation Co-efficient: ", correlation_coefficient1)
print(" ")
print("All Quantizaton details are Saved in files!")