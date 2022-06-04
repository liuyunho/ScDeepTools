import torch
import numpy as np
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

class Single_Cell_Data_Loader(Dataset):
    def __init__(self, data, lable=None):
        self.data = torch.Tensor(np.array(data)).to(torch.float32)
        if lable is None:
            self.lable = None
        else:
            self.lable = torch.Tensor(lable).to(torch.float32)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        if self.lable is None:
            return self.data[index], []
        else:
            return self.data[index], self.lable[index]

def GetDataLoader(scr_data, lables = None, class_num = None):
    if lables is None:
        dataset = Single_Cell_Data_Loader(scr_data, None)
    else:
        dataset = Single_Cell_Data_Loader(scr_data, np.eye(class_num)[np.array(lables)])
    data_loader = DataLoader(dataset, batch_size=300, shuffle=True)
    return data_loader
