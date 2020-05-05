import numpy as np
import argparse
import os



color_list = [
    '13130240',
    '32818',
    '56320',
    '16711680',
    '6579300',
    '13158600',
    '16711935',
    '16776960',
    '8388863',
    '16763030',
    '33023',
    '51455',
    '16744448'
]

def torgb(r, g, b):
    return (int(r) << 16 | int(g) << 8 | int(b))


def getFiles(path, suffix):
    return [os.path.join(root, file) for root, dirs, files in os.walk(path) for file in files if file.endswith(suffix)]


parser = argparse.ArgumentParser()
parser.add_argument('--data', '-d', default='../05',
                    help='data path')
parser.add_argument('--label', '-l', default='../results', help='label path')
parser.add_argument('--name','-n',required=True,help='name add on pcd file')
parser.add_argument('--mode','-m',default='color',help='output pred by color or label')

arg = parser.parse_args()

filelist = getFiles(arg.label, '.labels')

# print(filelist)

for fils in filelist:
    # print(fils)

    name = fils.split('.labels')[0].split('\\')[-1]
    #print(name, '\n')
    data = np.load(os.path.join(
        arg.data, name + '.npy'))
    label = np.loadtxt(fils)
    x = (np.max(data[:, 0])+np.min(data[:, 0]))/2
    y = (np.max(data[:, 1])+np.min(data[:, 1]))/2
    z = (np.max(data[:, 2])+np.min(data[:, 2]))/2
    data[:, 0] -= x
    data[:, 1] -= y
    data[:, 2] -= z

    print("processing ", name, '!!! pointcloud size: ', data.shape[0])

    file_orig = os.path.join('../orig_pcd', name + '_'+arg.name + '_orig.pcd')
    file_label = os.path.join('../label_pcd', name +'_'+ arg.name + '_label.pcd')
    file_pred = os.path.join('../pred_pcd', name +'_'+ arg.name + '_pred.pcd')

    if os.path.exists(file_orig):
        os.remove(file_orig)
    if os.path.exists(file_label):
        os.remove(file_label)
    if os.path.exists(file_pred):
        os.remove(file_pred)

    Output_orig = open(file_orig, "a",encoding='utf-8')
    Output_label = open(file_label, "a",encoding='utf-8')
    Output_pred = open(file_pred, "a",encoding='utf-8')
    
    if arg.mode is 'color':
        mode = 'rgb'
    else:
        mode = 'label'

    Output_pred.write('# .PCD v0.7 - Point Cloud Data file format\nVERSION 0.7\nFIELDS x y z '+mode+'\nSIZE 4 4 4 4 \nTYPE F F F U\nCOUNT 1 1 1 1')
    string = '\nWIDTH ' + str(data.shape[0])
    Output_pred.write(string)
    Output_pred.write('\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0')
    string = '\nPOINTS ' + str(data.shape[0])
    Output_pred.write(string)
    Output_pred.write('\nDATA ascii')

    Output_label.write(
        '# .PCD v0.7 - Point Cloud Data file format\nVERSION 0.7\nFIELDS x y z '+mode+'\nSIZE 4 4 4 4 \nTYPE F F F U\nCOUNT 1 1 1 1')
    string = '\nWIDTH ' + str(data.shape[0])
    Output_label.write(string)
    Output_label.write('\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0')
    string = '\nPOINTS ' + str(data.shape[0])
    Output_label.write(string)
    Output_label.write('\nDATA ascii')

    Output_orig.write(
        '# .PCD v0.7 - Point Cloud Data file format\nVERSION 0.7\nFIELDS x y z rgb\nSIZE 4 4 4 4 \nTYPE F F F U\nCOUNT 1 1 1 1')
    string = '\nWIDTH ' + str(data.shape[0])
    Output_orig.write(string)
    Output_orig.write('\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0')
    string = '\nPOINTS ' + str(data.shape[0])
    Output_orig.write(string)
    Output_orig.write('\nDATA ascii')

    if arg.mode is 'color':
        for j in range(data.shape[0]):
            string_xyz = ('\n' + str(data[j, 0]) + ' ' +str(data[j, 1]) + ' ' + str(data[j, 2]) + ' ')
            string = string_xyz+color_list[int(label[j]-1)]
            Output_pred.write(string)

            string = string_xyz+color_list[int(data[j, 6])]
            Output_label.write(string)

            string = string_xyz+str(torgb(data[j, 3],data[j, 4], data[j, 5]))
            Output_orig.write(string)

    else:
        for j in range(data.shape[0]):
            string_xyz = ('\n' + str(data[j, 0]) + ' ' +str(data[j, 1]) + ' ' + str(data[j, 2]) + ' ')
            string = string_xyz+str(int(label[j]-1))
            Output_pred.write(string)

            string = string_xyz+str(int(data[j, 6]))
            Output_label.write(string)
            string = string_xyz+str(torgb(data[j, 3],data[j, 4], data[j, 5]))
            Output_orig.write(string)

    Output_pred.close()
    Output_orig.close()
    Output_label.close()

print("all done!")


