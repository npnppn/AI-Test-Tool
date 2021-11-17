import os
import numpy as np

import torch
import torch.nn as nn

# 네트워크 저장하기


def save(ckpt_dir, net, optim, epoch, name, loss, iou, acc, lr, batch):
    if not os.path.exists(ckpt_dir):
        os.makedirs(ckpt_dir)

    torch.save({'net': net.state_dict(), 'optim': optim.state_dict(), 'epoch': epoch, 'loss': loss, 'iou': iou, 'acc': acc, 'lr': lr, 'batch': batch, 'name': name},
               "%s/%s_model.pth" % (ckpt_dir, name))


def best_save(ckpt_dir, net, optim, epoch, name, loss, iou, acc, lr, batch):
    if not os.path.exists(ckpt_dir):
        os.makedirs(ckpt_dir)
    torch.save({'net': net.state_dict(), 'optim': optim.state_dict(), 'epoch': epoch, 'loss': loss, 'iou': iou, 'acc': acc, 'lr': lr, 'batch': batch, 'name': name},
               "%s/%s_best_model.pth" % (ckpt_dir, name))

# 네트워크 불러오기


def load_compare(net, optim, path):
    if not os.path.exists(path):
        epoch = 0
        return net, optim, epoch

    dict_model = torch.load(path)

    net.load_state_dict(dict_model['net'])
    optim.load_state_dict(dict_model['optim'])
    epoch = dict_model['epoch']

    return net, optim, epoch


def load(ckpt_dir, net, optim, name):
    if not os.path.exists(ckpt_dir):
        epoch = 0
        return net, optim, epoch

    dict_model = torch.load('%s/%s' % (ckpt_dir, name))

    net.load_state_dict(dict_model['net'])
    optim.load_state_dict(dict_model['optim'])
    epoch = dict_model['epoch']

    return net, optim, epoch


def info_load(path):
    if not os.path.exists(path):
        return 0

    dict_model = torch.load(path)

    epoch = dict_model['epoch']
    loss = dict_model['loss']
    acc = dict_model['acc']
    iou = dict_model['iou']
    name = dict_model['name']
    batch = dict_model['batch']
    lr = dict_model['lr']

    return epoch, loss, acc, iou, name, batch, lr
