import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

path = './image_leather/'

dir_save_train = os.path.join(path, 'train')
dir_save_val = os.path.join(path, 'val')
dir_save_test = os.path.join(path, 'test')

if not os.path.exists(dir_save_train):
    os.makedirs(dir_save_train)

if not os.path.exists(dir_save_val):
    os.makedirs(dir_save_val)

if not os.path.exists(dir_save_test):
    os.makedirs(dir_save_test)


img_data = './image_leather/Imgs/'
labels_data = './image_leather/labels/'

nframe = len(os.listdir(img_data))

nframe_train = int(nframe * 3/4) 
nframe_val = int(nframe * 1/8) 
nframe_test = int(nframe * 1/8)


id_frame = np.arange(nframe)
np.random.shuffle(id_frame)
print(id_frame)


# ##
offset_nframe = 0

for i in range(nframe_train):
    img_label = Image.open(os.path.join(labels_data, os.listdir(
        labels_data)[id_frame[i + offset_nframe]]))
    img_label = img_label.resize((512, 512))
    img_input = Image.open(os.path.join(
        img_data, os.listdir(img_data)[id_frame[i + offset_nframe]]))
    img_input = img_input.resize((512, 512))
    img_input = img_input.convert('L')

    label_ = np.asarray(img_label)
    input_ = np.asarray(img_input)

    np.save(os.path.join(dir_save_train, 'label_%03d.npy' % i), label_)
    np.save(os.path.join(dir_save_train, 'input_%03d.npy' % i), input_)


##
offset_nframe = nframe_train

for i in range(nframe_val):
    img_label = Image.open(os.path.join(labels_data, os.listdir(
        labels_data)[id_frame[i + offset_nframe]]))
    img_label = img_label.resize((512, 512))
    img_input = Image.open(os.path.join(
        img_data, os.listdir(img_data)[id_frame[i + offset_nframe]]))
    img_input = img_input.resize((512, 512))
    img_input = img_input.convert('L')

    label_ = np.asarray(img_label)
    input_ = np.asarray(img_input)

    np.save(os.path.join(dir_save_val, 'label_%03d.npy' % i), label_)
    np.save(os.path.join(dir_save_val, 'input_%03d.npy' % i), input_)

##
offset_nframe = nframe_train + nframe_val

for i in range(nframe_test):
    img_label = Image.open(os.path.join(labels_data, os.listdir(
        labels_data)[id_frame[i + offset_nframe]]))
    img_label = img_label.resize((512, 512))
    img_input = Image.open(os.path.join(
        img_data, os.listdir(img_data)[id_frame[i + offset_nframe]]))
    img_input = img_input.resize((512, 512))
    img_input = img_input.convert('L')

    label_ = np.asarray(img_label)
    input_ = np.asarray(img_input)

    np.save(os.path.join(dir_save_test, 'label_%03d.npy' % i), label_)
    np.save(os.path.join(dir_save_test, 'input_%03d.npy' % i), input_)

##
plt.subplot(121)
plt.imshow(label_, cmap='gray')
plt.title('label')

plt.subplot(122)
plt.imshow(input_, cmap='gray')
plt.title('input')

plt.show()
