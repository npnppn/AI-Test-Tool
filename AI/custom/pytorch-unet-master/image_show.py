import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

path = './image/'

img_data = './image/Imgs/'
labels_data = './image/train/'

for i in range(len(os.listdir(labels_data))):
    img_array1 = np.load(labels_data + os.listdir(labels_data)[i])
    img_array2 = np.load(labels_data + os.listdir(labels_data)[i+89])
    plt.subplot(122)
    plt.imshow(img_array1, cmap='gray')
    plt.subplot(121)
    plt.imshow(img_array2, cmap='gray')
    plt.show()