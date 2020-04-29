

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os

import numpy as np


def getFiles(path, suffix):
    return [os.path.join(root, file) for root, dirs, files in os.walk(path) for file in files if file.endswith(suffix)]


# gt_label_filenames = []
# pred_label_filenames = []

DEFAULT_DATA_DIR = './05'
DEFAULT_PRED_DIR = './results'
NUM_CLASSES = 13

args = argparse.ArgumentParser()

args.add_argument(
    "-d", "--data", dest='data_dir',
    default=DEFAULT_DATA_DIR,
    help="Path to vkitti data (default is %s)" % DEFAULT_DATA_DIR)

args.add_argument("-pred", "--pred", default=DEFAULT_PRED_DIR,
                  help="path to prediction label,default is %s" % DEFAULT_PRED_DIR)

Args = args.parse_args()


pred_filelist = getFiles(Args.pred, '.labels')
gt_filelist = []

for files in pred_filelist:
    print(files)
    name = files.split(".labels")[0].split("\\")[-1]
    gt_dir = os.path.join(Args.data_dir, name + ".npy")
    if os.path.exists(gt_dir):
        gt_filelist.append(gt_dir)
        print(gt_dir)

num_file = len(pred_filelist)
num_gt = len(gt_filelist)

assert num_file == num_gt

gt_classes = [0] * NUM_CLASSES
positive_classes = [0] * NUM_CLASSES
true_positive_classes = [0] * NUM_CLASSES

print("Evaluating predictions:")

for i in range(num_file):
    pred_label = np.loadtxt(pred_filelist[i])
    gt_label = (np.load(gt_filelist[i]))
    gt_label = gt_label[:, -1]
    assert pred_label.shape[0] == gt_label.shape[0]
    print("calculating file", pred_filelist[i].split(
        ".labels")[0].split("\\")[-1], '...')
    for j in range(gt_label.shape[0]):
        gt_l = int(gt_label[j])
        pred_l = int(pred_label[j])
        gt_classes[gt_l] += 1
        positive_classes[pred_l-1] += 1
        true_positive_classes[gt_l] += int(gt_l == (pred_l-1))

class_name = ['Terrain', 'Tree', 'Vege', 'Building', 'Road', 'GuardRail',
              'Sign', 'Light', 'Pole', 'Misc', 'Truck', 'Car', 'Van']

print("Class name:\t{}".format('\t'.join(map(str, class_name))))
print("Classes:\t{}".format("\t".join(map(str, gt_classes))))
print("Positive:\t{}".format("\t".join(map(str, positive_classes))))
print("True positive:\t{}".format("\t".join(map(str, true_positive_classes))))
print("Overall accuracy: {0}".format(
    sum(true_positive_classes) / float(sum(positive_classes))))

print("Class IoU:")
iou_list = []
for i in range(13):
    if (gt_classes[i] == 0):
        iou = 0.0
    else:
        iou = true_positive_classes[i] / \
            float(gt_classes[i]+positive_classes[i]-true_positive_classes[i])
    print("  {}".format(iou))
    iou_list.append(iou)

print("Average IoU: {}".format(sum(iou_list)/13.0))
