# 라이브러리 추가하기
import argparse
from iou import *
import os
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from model import UNet
from dataset import *
from util import *
import matplotlib.pyplot as plt
from torchvision import transforms, datasets
import gc


def train(lr=0, batch_size=0, num_epoch=0, mode='test', name='', model1='train', model2=''):
    # train lr, batch_size, num_epoch,mode = 'test', name
    # test  lr, batch_size, num_epoch,mode='test',name, model1 = 해당 모델 경로
    # compare batch_size,mode='compare',model1 = 해당 모델 경로, model2 = 해당 모델 경로

    gc.collect()
    torch.cuda.empty_cache()

    lr = lr  # 학습횟수
    if lr == '':
        lr = None
    else:
        lr = float(lr)
    batch_size = batch_size
    if batch_size == '':
        batch_size = None
    else:
        batch_size = int(batch_size)
    num_epoch = num_epoch
    if num_epoch == '':
        num_epoch = None
    else:
        num_epoch = int(num_epoch)

    mode = mode
    train_continue = "off"
    name = name

    data_dir = "./datasets"  # 데이터셋 저장 디렉토리
    ckpt_dir = "./checkpoint/" + name
    log_dir = "./log/" + name  # tensorboard log 저장 디렉토리
    result_dir = "./result/" + name

    # compare/test1&test2/
    compare_dir = "./compare/" + \
                  os.path.basename(model1).replace(".pth", "") + "&" + \
                  os.path.basename(model2).replace(".pth", "")

    model_name = os.path.basename(model1)
    model1_name = model1
    model2_name = model2

    device = torch.device('cuda' if torch.cuda.is_available()
                          else 'cpu')  # gpu 혹은 cpu에서 동작할 지 결정해줌

    print("learning rate: %.4e" % lr)
    print("batch size: %d" % batch_size)
    print("number of epoch: %d" % num_epoch)
    print("data dir: %s" % data_dir)
    print("ckpt dir: %s" % ckpt_dir)
    print("log dir: %s" % log_dir)
    print("result dir: %s" % result_dir)
    print("mode: %s" % mode)

    # tensorboard 실행하기
    if mode == 'train':
        os.system("start cmd /c tensorboard --logdir={}".format(log_dir))

    if mode == 'test':
        print("test model %s" % model_name)
        # test 용 디렉토리 생성하기
        if not os.path.exists(result_dir):
            os.makedirs(os.path.join(result_dir, 'png/label'))
            os.makedirs(os.path.join(result_dir, 'png/input'))
            os.makedirs(os.path.join(result_dir, 'png/output'))
            os.makedirs(os.path.join(result_dir, 'numpy/label'))
            os.makedirs(os.path.join(result_dir, 'numpy/input'))
            os.makedirs(os.path.join(result_dir, 'numpy/output'))


    elif mode == 'compare':
        print("compare model1 %s" % model1_name)
        print("compare model2 %s" % model2_name)
        print("compare dir %s" % compare_dir)

    # compare 용 디렉토리 생성하기
    if mode == 'compare':
        if not os.path.exists(compare_dir):
            os.makedirs(os.path.join(compare_dir, 'png/label'))
            os.makedirs(os.path.join(compare_dir, 'png/input'))
            os.makedirs(os.path.join(compare_dir, 'png/output1'))
            os.makedirs(os.path.join(compare_dir, 'png/output2'))
            os.makedirs(os.path.join(compare_dir, 'numpy/label'))
            os.makedirs(os.path.join(compare_dir, 'numpy/input'))
            os.makedirs(os.path.join(compare_dir, 'numpy/output1'))
            os.makedirs(os.path.join(compare_dir, 'numpy/output2'))

    # 네트워크 학습하기
    if mode == 'train':
        transform = transforms.Compose(
            [Normalization(mean=0.5, std=0.5), RandomFlip(), ToTensor()])

        dataset_train = Dataset(data_dir=os.path.join(
            data_dir, 'train'), transform=transform)
        loader_train = DataLoader(
            dataset_train, batch_size=batch_size, shuffle=True, num_workers=0)

        dataset_val = Dataset(data_dir=os.path.join(
            data_dir, 'val'), transform=transform)
        loader_val = DataLoader(
            dataset_val, batch_size=batch_size, shuffle=False, num_workers=0)

        # 그밖에 부수적인 variables 설정하기
        num_data_train = len(dataset_train)
        num_data_val = len(dataset_val)

        num_batch_train = np.ceil(num_data_train / batch_size)
        num_batch_val = np.ceil(num_data_val / batch_size)
    else:
        transform = transforms.Compose(
            [Normalization(mean=0.5, std=0.5), ToTensor()])

        dataset_test = Dataset(data_dir=os.path.join(
            data_dir, 'test'), transform=transform)
        loader_test = DataLoader(
            dataset_test, batch_size=batch_size, shuffle=False, num_workers=0)

        # 그밖에 부수적인 variables 설정하기
        num_data_test = len(dataset_test)

        num_batch_test = np.ceil(num_data_test / batch_size)

    # 네트워크 생성하기
    net = UNet().to(device)
    if mode == 'compare':
        net1 = UNet().to(device)
        net2 = UNet().to(device)

    # 손실함수 정의하기
    fn_loss = nn.BCEWithLogitsLoss().to(device)

    # Optimizer 설정하기
    optim = torch.optim.Adam(net.parameters(), lr=lr)

    # 그밖에 부수적인 functions 설정하기

    def fn_tonumpy(x):
        return x.to(
            'cpu').detach().numpy().transpose(0, 2, 3, 1)

    def fn_denorm(x, mean, std):
        return (x * std) + mean

    def fn_class(x):
        return 1.0 * (x > 0.5)

    # Tensorboard 를 사용하기 위한 SummaryWriter 설정
    writer_train = SummaryWriter(log_dir=os.path.join(log_dir, 'train'))
    writer_val = SummaryWriter(log_dir=os.path.join(log_dir, 'val'))

    # 네트워크 학습시키기
    st_epoch = 0

    # TRAIN MODE
    if mode == 'train':
        best_loss = 100
        if train_continue == "on":
            net, optim, st_epoch = load(
                ckpt_dir=ckpt_dir, net=net, optim=optim)

        for epoch in range(st_epoch + 1, num_epoch + 1):
            net.train()
            loss_arr = []
            iou_arr = []
            for batch, data in enumerate(loader_train, 1):
                # forward pass
                label = data['label'].to(device)
                input = data['input'].to(device)

                output = net(input)

                # backward pass
                optim.zero_grad()

                loss = fn_loss(output, label)
                loss.backward()

                optim.step()

                # 손실함수 계산
                loss_arr += [loss.item()]

                # Tensorboard 저장하기
                label = fn_tonumpy(label)
                input = fn_tonumpy(fn_denorm(input, mean=0.5, std=0.5))
                output = fn_tonumpy(fn_class(output))

                iou = iou_numpy(output, label)
                iou_arr += [iou]
                acc = np.mean(output == label) * 100

                print("TRAIN: EPOCH %04d / %04d | BATCH %04d / %04d | LOSS %.4f | IoU %.4f | ACC %.4f" %
                      (epoch, num_epoch, batch, num_batch_train, np.mean(loss_arr), iou, acc))

                writer_train.add_image(
                    'label', label, num_batch_train * (epoch - 1) + batch, dataformats='NHWC')
                writer_train.add_image(
                    'input', input, num_batch_train * (epoch - 1) + batch, dataformats='NHWC')
                writer_train.add_image(
                    'output', output, num_batch_train * (epoch - 1) + batch, dataformats='NHWC')

            writer_train.add_scalar('loss', np.mean(loss_arr), epoch)
            writer_train.add_scalar('iou', np.mean(iou_arr), epoch)

            with torch.no_grad():
                net.eval()
                loss_arr = []
                iou_arr = []
                acc = 0
                for batch, data in enumerate(loader_val, 1):
                    # forward pass
                    label = data['label'].to(device)
                    input = data['input'].to(device)

                    output = net(input)

                    # 손실함수 계산하기
                    loss = fn_loss(output, label)

                    loss_arr += [loss.item()]

                    # Tensorboard 저장하기
                    label = fn_tonumpy(label)
                    input = fn_tonumpy(fn_denorm(input, mean=0.5, std=0.5))
                    output = fn_tonumpy(fn_class(output))

                    iou = iou_numpy(output, label)
                    iou_arr += [iou]
                    acc = np.mean(output == label) * 100

                    print("VALID: EPOCH %04d / %04d | BATCH %04d / %04d | LOSS %.4f | IoU %.4f | ACC %.4f" %
                          (epoch, num_epoch, batch, num_batch_val, np.mean(loss_arr), iou, acc))
                    # VALID에서 Best LOSS
                    if best_loss > np.mean(loss_arr):
                        best_loss = np.mean(loss_arr)
                        # SAVE
                        best_save(ckpt_dir=ckpt_dir, net=net,
                                  optim=optim, epoch=epoch, name=name, loss=np.mean(loss_arr), iou=np.mean(iou_arr),
                                  acc=acc, lr=lr, batch=batch_size)

                    writer_val.add_image(
                        'label', label, num_batch_val * (epoch - 1) + batch, dataformats='NHWC')
                    writer_val.add_image(
                        'input', input, num_batch_val * (epoch - 1) + batch, dataformats='NHWC')
                    writer_val.add_image(
                        'output', output, num_batch_val * (epoch - 1) + batch, dataformats='NHWC')

            writer_val.add_scalar('loss', np.mean(loss_arr), epoch)
            writer_val.add_scalar('iou', np.mean(iou_arr), epoch)

            if epoch == num_epoch:
                save(ckpt_dir=ckpt_dir, net=net,
                     optim=optim, epoch=epoch, name=name, loss=np.mean(loss_arr), iou=np.mean(iou_arr), acc=acc, lr=lr,
                     batch=batch_size)

        writer_train.close()
        writer_val.close()

    # TEST MODE
    elif mode == 'test':
        net, optim, st_epoch = load(
            ckpt_dir=ckpt_dir, net=net, optim=optim, name=model_name)

        with torch.no_grad():
            net.eval()
            loss_arr = []
            iou_arr = []
            acc_arr = []

            for batch, data in enumerate(loader_test, 1):
                # forward pass
                label = data['label'].to(device)
                input = data['input'].to(device)

                output = net(input)

                # 손실함수 계산하기
                loss = fn_loss(output, label)

                loss_arr += [loss.item()]

                # Tensorboard 저장하기
                label = fn_tonumpy(label)
                input = fn_tonumpy(fn_denorm(input, mean=0.5, std=0.5))
                output = fn_tonumpy(fn_class(output))

                iou = iou_numpy(output, label)
                iou_arr += [iou]
                acc = np.mean(output == label) * 100
                acc_arr += [acc]

                print("TEST: BATCH %04d / %04d | LOSS %.4f | IoU %.4f | ACC %.4f" %
                      (batch, num_batch_test, np.mean(loss_arr), iou, acc))

                for j in range(label.shape[0]):
                    id = num_batch_test * (batch - 1) + j

                    plt.imsave(os.path.join(result_dir, 'png/label', 'label_%04d.png' %
                                            id), label[j].squeeze(), cmap='gray')
                    plt.imsave(os.path.join(result_dir, 'png/input', 'input_%04d.png' %
                                            id), input[j].squeeze(), cmap='gray')
                    plt.imsave(os.path.join(result_dir, 'png/output', 'output_%04d.png' %
                                            id), output[j].squeeze(), cmap='gray')

                    np.save(os.path.join(result_dir, 'numpy/label',
                                         'label_%04d.npy' % id), label[j].squeeze())
                    np.save(os.path.join(result_dir, 'numpy/input',
                                         'input_%04d.npy' % id), input[j].squeeze())
                    np.save(os.path.join(result_dir, 'numpy/output',
                                         'output_%04d.npy' % id), output[j].squeeze())

        print("AVERAGE TEST: BATCH %04d / %04d | LOSS %.4f | IoU %.4f | ACC %.4f" %
              (batch, num_batch_test, np.mean(loss_arr), np.mean(iou_arr), np.mean(acc_arr)))

    # COMPARE MODE
    else:
        net1, optim1, st_epoch1 = load_compare(
            net=net1, optim=optim, path=model1_name)

        net2, optim2, st_epoch2 = load_compare(
            net=net2, optim=optim, path=model2_name)

        with torch.no_grad():
            net1.eval()
            net2.eval()
            loss_arr1 = []
            iou_arr1 = []
            loss_arr2 = []
            iou_arr2 = []
            acc_arr1 = []
            acc_arr2 = []

            for batch, data in enumerate(loader_test, 1):
                # forward pass
                label = data['label'].to(device)
                input = data['input'].to(device)

                output1 = net1(input)

                # 손실함수 계산하기
                loss1 = fn_loss(output1, label)

                loss_arr1 += [loss1.item()]

                output2 = net2(input)

                # 손실함수 계산하기
                loss2 = fn_loss(output2, label)

                loss_arr2 += [loss2.item()]

                # Tensorboard 저장하기
                label = fn_tonumpy(label)
                input = fn_tonumpy(fn_denorm(input, mean=0.5, std=0.5))
                output1 = fn_tonumpy(fn_class(output1))
                output2 = fn_tonumpy(fn_class(output2))

                iou1 = iou_numpy(output1, label)
                iou_arr1 += [iou1]

                iou2 = iou_numpy(output2, label)
                iou_arr2 += [iou2]

                acc1 = np.mean(output1 == label) * 100
                acc_arr1 += [acc1]

                acc2 = np.mean(output2 == label) * 100
                acc_arr2 += [acc2]

                print("TEST1: BATCH %04d / %04d | LOSS %.4f | IoU %.4f | ACC %.4f" %
                      (batch, num_batch_test, np.mean(loss_arr1), iou1, acc1))

                print("TEST2: BATCH %04d / %04d | LOSS %.4f | IoU %.4f | ACC %.4f" %
                      (batch, num_batch_test, np.mean(loss_arr2), iou2, acc2))

                for j in range(label.shape[0]):
                    id = num_batch_test * (batch - 1) + j

                    plt.imsave(os.path.join(compare_dir, 'png/label', 'label_%04d.png' %
                                            id), label[j].squeeze(), cmap='gray')
                    plt.imsave(os.path.join(compare_dir, 'png/input', 'input_%04d.png' %
                                            id), input[j].squeeze(), cmap='gray')
                    plt.imsave(os.path.join(compare_dir, 'png/output1', 'output1_%04d.png' %
                                            id), output1[j].squeeze(), cmap='gray')
                    plt.imsave(os.path.join(compare_dir, 'png/output2', 'output2_%04d.png' %
                                            id), output2[j].squeeze(), cmap='gray')

                    np.save(os.path.join(compare_dir, 'numpy/label',
                                         'label_%04d.npy' % id), label[j].squeeze())
                    np.save(os.path.join(compare_dir, 'numpy/input',
                                         'input_%04d.npy' % id), input[j].squeeze())
                    np.save(os.path.join(compare_dir, 'numpy/output1',
                                         'output1_%04d.npy' % id), output1[j].squeeze())
                    np.save(os.path.join(compare_dir, 'numpy/output2',
                                         'output2_%04d.npy' % id), output2[j].squeeze())

        print("AVERAGE TEST1: BATCH %04d / %04d | LOSS %.4f | IoU %.4f | ACC %.4f" %
              (batch, num_batch_test, np.mean(loss_arr1), np.mean(iou_arr1), np.mean(acc_arr1)))
        print("AVERAGE TEST2: BATCH %04d / %04d | LOSS %.4f | IoU %.4f| ACC %.4f" %
              (batch, num_batch_test, np.mean(loss_arr2), np.mean(iou_arr2), np.mean(acc_arr2)))
