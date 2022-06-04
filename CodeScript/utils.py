import numpy as np
import pandas as pd
from collections import defaultdict, Counter
from sklearn.decomposition import PCA
import torch
from numbers import Number
import umap
import random
import matplotlib.pyplot as plt

class Single_Cell_Data:
    def __init__(self, Identifer, Dimension1, Dimension2, Lables, Color_dic, label_tags=None):
        self.identifer = Identifer
        self.x = Dimension1
        self.y = Dimension2
        if label_tags:
            self.label = [label_tags[lab] for lab in Lables]
            self.color_dict = {label_tags[lab]:Color_dic[lab] for lab in Color_dic}
        else:
            self.label = Lables
            self.color_dict = Color_dic
        self.group, self.group_len, self.group_col = self._creat_group()
    def _creat_group(self):
        group = defaultdict(dict)
        index=0
        for lab in self.label:
            if not group[lab]:
                group[lab]['x'] = []
                group[lab]['y'] = []
                group[lab]['identifer'] = []
                group[lab]['index'] = []
                group[lab]['label'] = []
            group[lab]['x'].append(self.x[index])
            group[lab]['y'].append(self.y[index])
            group[lab]['index'].append(index)
            group[lab]['identifer'].append(self.identifer[index])
            group[lab]['label'].append(self.label[index])
            index+=1
        group_col, group_len=defaultdict(), defaultdict()
        for lab in group:
            group_col[lab] = self.color_dict[lab]
            group_len[lab] = len(group[lab]['x'])
        return group, group_len, group_col

def Sel_Gene_by_Proportion(data,low_ratio=0.4,high_ratio=0.9):
    sel_index=[]
    assert isinstance(data,pd.DataFrame), 'Input must be pandas.dataframe!'
    for i in range(len(data)):
        if np.sum(data.iloc[i]==0)/data.shape[1] < high_ratio and np.sum(data.iloc[i]==0)/data.shape[1] > low_ratio:
            sel_index.append(i)
    return data.iloc[sel_index]

def accuracy_and_recovery(pre,rel):
    pre=np.array(pre)
    rel=np.array(rel)
    result_dic=defaultdict(list)
    rel_dic=Counter(rel)
    pre_dic=Counter(pre)
    #get result dictionary
    for key in pre_dic:
        aa=Counter(rel[pre==key])
        result_dic[(key,max(aa,key=aa.get))]=[max(aa.values()),sum(aa.values())]
    clu_acc = defaultdict()
    lab_info = defaultdict(list)
    for key,value in result_dic.items():
        #get cluster accuracy
        clu_acc[key]=value[0]/value[1]
        #get the lab information
        lab_info[key[1]].append(value)
    lab_acc = defaultdict()
    lab_rec = defaultdict()
    for key,value in lab_info.items():
        #get label accuracy
        _rig=sum([en[0] for en in value])
        _all=sum([en[1] for en in value])
        lab_acc[key]=_rig/_all
        #get label recovery
        lab_rec[key]=_rig/rel_dic[key]
    return dict(clu_acc),dict(lab_acc),dict(lab_rec)


def to_ndarray(x):
    if type(x) is Number:
        return np.array(x)

    elif type(x) is np.ndarray:
        return x

    elif type(x) is torch.Tensor:
        return x.detach().cpu().numpy()


def LabelIndexTrans(pre_labels):
    lables = []
    coun = Counter(pre_labels)
    index = 0
    for key in coun:
        coun[key] = index
        index += 1
    for lab in pre_labels:
        lables.append(coun[lab])
    return lables, coun

def DataReader(data_path,tag_path=None,low_ratio=0.4,high_ratio=0.9):
    data = pd.read_csv(data_path)
    data.index = data['Unnamed: 0']
    del data['Unnamed: 0']
    data = Sel_Gene_by_Proportion(data,low_ratio=low_ratio,high_ratio=high_ratio)
    print('******The gene screening result is as follows:******')
    print('Cell number: %d' % data.shape[1])
    print('Screened gene number: %d' % data.shape[0])
    if tag_path is None:
        return data
    label = pd.read_csv(tag_path)
    labelT, labelmap= LabelIndexTrans(label.iloc[:,1])
    labelsum = Counter(label.iloc[:,1])
    mapR = pd.DataFrame([labelsum,labelmap]).T
    mapR.columns=['cell_number','map_index']
    print('The labels summary and re-assignment index mapping are as follows:')
    print(mapR)
    return data, labelT, mapR

def GetIntersectedFeature(data_file, beta_file):
    data = pd.read_csv(data_file)
    data.index = data['Unnamed: 0']
    del data['Unnamed: 0']
    beta = pd.read_csv(beta_file)
    beta.index = beta['Unnamed: 0']
    del beta['Unnamed: 0']
    di, bi=[], []
    for i in range(data.shape[0]):
        if data.index.tolist()[i] in beta.columns:
            di.append(i)
            bi.append(beta.columns.tolist().index(data.index.tolist()[i]))
    return data.iloc[np.array(di),:], beta.iloc[:,np.array(bi)]

def RandCor():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ''.join([colorArr[random.randint(0, 14)] for _ in range(6)])
    return '#' + color


def PlotClass(coor1, coor2, label, color, size):
    colors = [color[each] for each in label]
    plt.figure(figsize=size)
    plt.scatter(x=coor1, y=coor2, c=colors, s=5)
    # legend
    for lab in color.keys():
        plt.scatter([], [], c=color[lab], s=20, label=lab)
    plt.legend(frameon=False)
    # plt.show()


def PlotGradient(coor1, coor2, atrr, size, cmap):
    plt.figure(figsize=size)
    plt.scatter(x=coor1, y=coor2, c=atrr, s=5, cmap=cmap)
    plt.colorbar()
    # plt.show()


def GetCentral(coor1, coor2, label):
    central = dict()
    for lab in Counter(label):
        index = np.array(label) == lab
        central[lab] = [np.mean(np.array(coor1)[index]), np.mean(np.array(coor2)[index])]
    return central


def PlotCellDistribution(count, cell_coor1=None, cell_coor2=None, pca_n=30,
                         cell_label=None, color_dict=None, map_atrr=None, cmap='spring', size=(8, 6), seed=42):
    return_index = 0
    if cell_coor1 is None or cell_coor2 is None:
        return_index += 2
        pca = PCA(n_components=pca_n)
        pca.fit(count)
        reducer = umap.UMAP(random_state=seed)
        reduce_data = pca.fit_transform(count)
        embedding = reducer.fit_transform(reduce_data)
        cell_coor1, cell_coor2 = embedding[:, 0], embedding[:, 1]

    if map_atrr is not None:
        PlotGradient(cell_coor1, cell_coor2, map_atrr, size, cmap)

    else:
        if cell_label is None:
            cell_label = ['cell' for _ in count.shape[0]]
        if color_dict is None:
            return_index += 3
            color_dict = dict()
            lab_item = Counter(cell_label)
            for lab in lab_item:
                radc = RandCor()
                if radc not in color_dict.values():
                    color_dict[lab] = radc
        PlotClass(cell_coor1, cell_coor2, cell_label, color_dict, size)
        # position label
        if len(color_dict) > 1:
            centra = GetCentral(cell_coor1, cell_coor2, cell_label)
            for lab in centra:
                plt.annotate(lab, xy=(centra[lab][0], centra[lab][1]), xytext=(centra[lab][0], centra[lab][1]))
    plt.show()

    if return_index == 5:
        return [cell_coor1, cell_coor2, color_dict]
    elif return_index == 2:
        return [cell_coor1, cell_coor2]
    elif return_index == 3:
        return [color_dict]
