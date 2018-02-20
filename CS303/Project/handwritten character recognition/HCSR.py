import os
import numpy as np
import pickle

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
import random
import math
import sys
import copy

# Definition of functions and parameters
# for example


# 1. Data preprocessing: normalize all pixels to [0,1) by dividing 256
def normalize_data(train_image, test_image):
    train_image = train_image / 255
    test_image = test_image / 255
    return train_image, test_image
    # for i in range(0, 10000):
    #     for j in range(0, 784):
    #         train_images[i, j] = train_images[i, j]/255


### 2. Weight initialization: Xavier
def weight_initialization(w):
    shape1 = w[0].shape[0]+w[0].shape[1]
    shape2 = w[1].shape[0]+w[1].shape[1]
    shape3 = w[2].shape[0]+w[2].shape[1]
    for i in range(0, w[1].shape[0]):
        for j in range(0, w[0].shape[1]):
            w[0][i, j] = random.uniform(-math.sqrt(6)/math.sqrt(shape1), math.sqrt(6)/math.sqrt(shape1))
    for i in range(0, w[1].shape[0]):
        for j in range(0, w[1].shape[1]):
            w[1][i, j] = random.uniform(-math.sqrt(6)/math.sqrt(shape2), math.sqrt(6)/math.sqrt(shape2))
    for i in range(0, w[2].shape[0]):
        for j in range(0, w[2].shape[1]):
            w[2][i, j] = random.uniform(-math.sqrt(6)/math.sqrt(shape3), math.sqrt(6)/math.sqrt(shape3))
    return w

# 3. training of neural network
# loss = np.zeros((EPOCH))
# accuracy = np.zeros((EPOCH))
# for epoch in range(0, EPOCH):
#     print(epoch)


# Forward propagation
def forward_propagation(dat, w, a, z, b, p):
    a[0] = np.add(np.dot(dat, w[0]), b[0])
    # z[0] = np.maximum(0, a[0])
    # print(z[0])
    # p[0] = np.where(p[0] < 0, a[0], 1)
    # p[0] = np.where(p[0] > 0, a[0], 0)
    for i in range(0, z[0].shape[0]):
        for j in range(0, z[0].shape[1]):
            z[0][i, j] = max(0, a[0][i, j])
            if a[0][i, j] > 0:
                p[0][i, j] = 1
    a[1] = np.add(np.dot(z[0], w[1]), b[1])
    # z[1] = np.maximum(0, a[1])
    # print(z[1])
    # p[1] = np.where(p[1] < 0, a[1], 1)
    # p[1] = np.where(p[1] > 0, a[1], 0)
    for i in range(0, z[1].shape[0]):
        for j in range(0, z[1].shape[1]):
            z[1][i, j] = max(0, a[1][i, j])
            if a[1][i, j] > 0:
                p[1][i, j] = 1
    a[2] = np.add(np.dot(z[1], w[2]), b[2])
    for i in range(0, a[2].shape[0]):
        summary = 0
        for j in range(0, a[2].shape[1]):
            summary = summary+math.exp(a[2][i, j])
        for j in range(0, a[2].shape[1]):
            z[2][i, j] = math.exp(a[2][i, j])/summary
    return a, z, p


# Back propagation
# Gradient update
def gradient_update(dat, rate, result, w, z, s, p, b):
    s[2] = z[2]-result
    s[1] = np.dot(s[2], w[2].T) * p[1]
    s[0] = np.dot(s[1], w[1].T) * p[0]
    w[2] = w[2]-(rate*np.dot(z[1].T, s[2])-rate*constant_lambda*w[2])/100
    change1 = np.zeros(b[2].shape[1])
    for i in range(0, b[2].shape[1]):
        for j in range(0, b[2].shape[0]):
            change1[i] = change1[i]+s[2][j, i]
        for j in range(0, b[2].shape[0]):
            b[2][j, i] = b[2][j, i]-rate*change1[i]/100
    w[1] = w[1]-(rate*np.dot(z[0].T, s[1])-rate*constant_lambda*w[1])/100
    change2 = np.zeros(b[1].shape[1])
    for i in range(0, b[1].shape[1]):
        for j in range(0, b[1].shape[0]):
            change2[i] = change2[i] + s[1][j, i]
        for j in range(0, b[1].shape[0]):
            b[1][j, i] = b[1][j, i] - rate * change2[i] / 100
    w[0] = w[0]-(rate*np.dot(dat.T, s[0])-rate*constant_lambda*w[0])/100
    change3 = np.zeros(b[0].shape[1])
    for i in range(0, b[0].shape[1]):
        for j in range(0, b[0].shape[0]):
            change3[i] = change3[i] + s[0][j, i]
        for j in range(0, b[0].shape[0]):
            b[0][j, i] = b[0][j, i] - rate * change3[i] / 100
    return s, w, b

    # weight2 = np.subtract(weight2, )




# Testing for accuracy
### 4. Plot
# for example
# plt.figure(figsize=(12,5))
# ax1 = plt.subplot(111)
# ax1.plot(......)
# plt.xlabel(......)
# plt.ylabel(......)
# plt.grid()
# plt.tight_layout()
# plt.savefig('figure.pdf', dbi=300)
if __name__ == "__main__":
    EPOCH = 100
    constant_lambda = 0.0005
    # Read all data from .pkl
    (train_images, train_labels, test_images, test_labels) = pickle.load(open('./mnist_data/data.pkl', 'rb'),encoding='latin1')
    total_loss = []
    accuracy = []
    train_loss = []
    # normalize data
    train_images, test_images = normalize_data(train_images, test_images)
    weight1 = np.zeros((784, 300))
    weight2 = np.zeros((300, 100))
    weight3 = np.zeros((100, 10))
    weight = [weight1, weight2, weight3]
    a1 = np.zeros((100, 300))
    z1 = np.zeros((100, 300))
    a2 = np.zeros((100, 100))
    z2 = np.zeros((100, 100))
    a3 = np.zeros((100, 10))
    z3 = np.zeros((100, 10))
    active = [a1, a2, a3]
    z_active = [z1, z2, z3]
    b1 = np.zeros((100, 300))
    b2 = np.zeros((100, 100))
    b3 = np.zeros((100, 10))
    beside = [b1, b2, b3]
    data = np.zeros((100, 784))
    sigma1 = np.zeros((100, 300))
    sigma2 = np.zeros((100, 100))
    sigma3 = np.zeros((100, 10))
    sigma = [sigma1, sigma2, sigma3]
    plot_index = np.zeros(100)
    for index in range(0, len(plot_index)):
        plot_index[index] = index+1
    # initialize weight
    weight = weight_initialization(weight)
    for epoch in range(0, 100):
        loss = 0
        pre_right = 0
        train_loss_epoch = 0
        for iteration in range(0, 100):
            partial1 = np.zeros((100, 300))
            partial2 = np.zeros((100, 100))
            partial3 = np.zeros((100, 10))
            partial = [partial1, partial2, partial3]
            if epoch < 50:
                learning_rate = 0.1
            else:
                learning_rate = 0.01
            results = np.zeros((100, 10))
            for index in range(0, 100):
                data[index] = train_images[iteration*100+index]
                results[index, train_labels[iteration*100+index]] = 1
            #   forward_propagation(dat, w, a, z, b, p):   return a, z, p
            active, z_active, partial = forward_propagation(data, weight, active, z_active, beside, partial)
            # gradient_update(dat, rate, result, w, z, s, p, b)  return s, w, b
            sigma, weight, beside = gradient_update(data, learning_rate, results, weight, z_active, sigma, partial, beside)
            for index in range(0, 100):
                train_loss_epoch += -np.log(z_active[2][index, train_labels[iteration*100+index]])
        for iteration in range(0, 10):
            for index in range(0, 100):
                data[index] = test_images[iteration * 100 + index]
            result_z_active = z_active
            result_active = active
            result_active, result_z_active, result_partial = forward_propagation(data, weight, result_active, result_z_active,beside,partial)
            for index in range(0, 100):
                loss += -np.log(result_z_active[2][index, test_labels[iteration*100+index]])
                maximum = -float('inf')
                number = None
                for find in range(0, 10):
                    if result_z_active[2][index, find] > maximum:
                        maximum = result_z_active[2][index, find]
                        number = find
                if number == test_labels[iteration*100+index]:
                    pre_right += 1
        pre_right = pre_right/1000
        train_loss.append(train_loss_epoch)
        print("epoch", epoch)
        print("train set loss", train_loss_epoch)
        print("test set loss", loss)
        total_loss.append(loss)
        print("accuracy", pre_right*100, "%")
        accuracy.append(pre_right)
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(7, 10))
    # print test set loss
    ax0.set_title('Loss')
    ax0.plot(plot_index, total_loss)
    ax0.set_xlabel('epoch')
    # print test set accuracy
    ax1.set_title('Accuracy')
    ax1.plot(plot_index, accuracy)
    ax1.set_xlabel('epoch')
    # print train set loss
    ax2.set_title('Train loss')
    ax2.plot(plot_index, train_loss)
    ax2.set_xlabel('epoch')
    plt.tight_layout()
    plt.savefig("train.png", dpi=300)









