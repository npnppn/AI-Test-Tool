import os
import numpy as np

import torch
import torch.nn as nn

# 네트워크 저장하기


def save(ckpt_dir, net, optim, epoch, name, loss, iou):
    if not os.path.exists(ckpt_dir):
        os.makedirs(ckpt_dir)

    torch.save({'net': net.state_dict(), 'optim': optim.state_dict(), 'epoch': epoch, 'loss': loss, 'iou': iou},
               "%s/%s_model.pth" % (ckpt_dir, name))


def best_save(ckpt_dir, net, optim, epoch, name, loss, iou):
    if not os.path.exists(ckpt_dir):
        os.makedirs(ckpt_dir)
    torch.save({'net': net.state_dict(), 'optim': optim.state_dict(), 'epoch': epoch, 'loss': loss, 'iou': iou},
               "%s/%s_best_loss_model.pth" % (ckpt_dir, name))

# 네트워크 불러오기


def load(ckpt_dir, net, optim, name):
    if not os.path.exists(ckpt_dir):
        epoch = 0
        return net, optim, epoch

    dict_model = torch.load('%s/%s' % (ckpt_dir, name))

    net.load_state_dict(dict_model['net'])
    optim.load_state_dict(dict_model['optim'])
    epoch = dict_model['epoch']
    loss = dict_model['loss']

    return net, optim, epoch
