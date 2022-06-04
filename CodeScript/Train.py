from Deep_LDA import LDAModel
from Impurity_Inference import SemiModel
from Pseudo_Inference import GenerateModel
import torch
import pyro
from tqdm import trange
from pyro.optim import ClippedAdam
from pyro.infer import SVI, TraceMeanField_ELBO, TraceEnum_ELBO, config_enumerate
import os
import time

'''Will upload soon
If there are any questions, please contact yunhe_liu15@fudan.edu.cn
'''