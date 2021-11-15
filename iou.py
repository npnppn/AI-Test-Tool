import torch
import numpy as np

SMOOTH = 1e-6


def iou_numpy(outputs: np.array, labels: np.array):

    outputs = outputs.squeeze(3)
    labels = labels.squeeze(3)

    outputs = outputs.astype(int)
    labels = labels.astype(int)

    intersection = (outputs & labels).sum((1, 2))

    union = (outputs | labels).sum((1, 2))

    iou = (intersection + SMOOTH) / (union + SMOOTH)

    thresholded = np.ceil(np.clip(20 * (iou - 0.5), 0, 10)) / 10

    return thresholded.mean()
