import os
import numpy as np
import argparse

arg = argparse.ArgumentParser()

roots = "./05"

arg.add_argument("-f", "--folder", default=roots)

Arg = arg.parse_args()

root = Arg.folder

if os.path.exists("filelist.txt"):
    os.remove("filelist.txt")

file = open("filelist.txt", mode="w")


def getFiles(path, suffix):
    return [os.path.join(root, file) for root, dirs, files in os.walk(path) for file in files if file.endswith(suffix)]


sublist = getFiles(root, ".npy")
for sublists in sublist:
    data = np.load(sublists)
    strs = sublists.split('.npy')[0].split('\\')[-1]
    print(strs)
    strs = "\""+strs+"\": ["+str(np.size(data, axis=0))+", \"" + strs+"\"],"
    file.writelines(strs+'\n')


file.close()
