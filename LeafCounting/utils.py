import numpy as np
import cv2
from PIL import Image,ImageOps
import pandas as pd
from keras.applications.resnet50 import preprocess_input

# boundaries for green color
boundaries = [
    # ([33, 140, 0], [140, 255, 255])
    ([33, 80, 40], [105, 255, 255])
]
(lower, upper) = boundaries[0]
lower = np.array(lower, dtype="uint8")
upper = np.array(upper, dtype="uint8")

def extract_leaf(np_image):
    hsvIm = cv2.cvtColor(np_image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsvIm, lower, upper)

    element = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    mask = cv2.erode(mask, element, iterations=1)
    mask = cv2.dilate(mask, element, iterations=1)
    mask = cv2.erode(mask, element)
    output = cv2.bitwise_and(hsvIm, hsvIm, mask=mask)

    return output

# vizualize results in train and validation set
# x, y is list, type is string
def vizualize_results(x, y, type):
    import matplotlib.pyplot as plt
    plt.plot(x)
    plt.plot(y)
    plt.title('Model '+type)
    plt.ylabel(type)
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

# read model loss file and return list of loss
def read_loss_txt(filename):
    loss = []
    f = open(filename)
    for line in f:
        loss.append(float(line.strip('\n')))
    return loss

# function is used when using colab
def read_csv_loss_file(filename):
  colnames = ['val_loss','val_mse', 'loss', 'mse']
  with open(filename, mode='r') as f:
    data = pd.read_csv(filename, names=colnames)
  return data


def get_loss(data):
    loss = data.loss.tolist()
    val_loss = data.val_loss.tolist()
    mse = data.mse.tolist()
    val_mse = data.val_mse.tolist()

    loss.pop(0)
    val_loss.pop(0)
    mse.pop(0)
    val_mse.pop(0)

    for i in range(len(loss)):
        loss[i] = float(loss[i])

    for i in range(len(val_loss)):
        val_loss[i] = float(val_loss[i])

    for i in range(len(mse)):
        mse[i] = float(mse[i])

    for i in range(len(val_mse)):
        val_mse[i] = float(val_mse[i])

    return (loss, val_loss, mse, val_mse)

def read_loss_csv(filename):
  data = read_csv_loss_file(filename)
  return get_loss(data)

def save_loss(filename, loss):
  with open(filename, 'w') as f:
    for ls in loss:
        f.write("%s\n" % ls)

def load_image(filename, size):
    img = Image.open(filename)
    img = img.resize(size)
    image = np.asarray(img)[:, :, 0:3]

    return image

# preprocess input image
def preprocess_image(filename, size):
    image = load_image(filename, size)
    image = preprocess_input(image)

    return image

