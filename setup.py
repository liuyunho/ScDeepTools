#! /usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='ScDeepTools',  
    author='Yunhe Liu', 
    version='0.1.0',  
    license='Apache License 2.0',
    packages=['Pseudo_Inference','CodeScript','Deep_LDA','Impurity_Inference','Distribution_Plot'],
    description='The software includes three deep generative models, a pseudo-cell inference model, a noisy cell inference model, and an LDA-based inference model for cell classification and class-specific genes analysis. Moreover, the software includes an interactive single-cell sequencing cell distribution mapping tool for manipulation of cell deletion and export.',  # 描述
    author_email='yunhe_liu15@fudan.edu.cn',  
    url='https://github.com/liuyunho/ScDeepTools',  

    install_requires=[
        'numpy >= 1.18.5',
        'pandas >= 0.23.0',
        'matplotlib >= 2.2.2',
        'torch >= 1.8.1',
        'pyro-ppl >= 1.7.0',
        'tqdm >= 4.62.0',
        'sklearn >= 0.0',
        'umap-learn >= 0.5.1'
    ],
    entry_points={ 
        'console_scripts': [
            'Pseudo_Inference=Pseudo_Inference.__main__:main',
            'Impurity_Inference=Impurity_Inference.__main__:main',
            'Deep_LDA=Deep_LDA.__main__:main'
        ]
    },
    classifiers=['License :: OSI Approved :: BSD 3-Clause "New" or "Revised" License',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence',
                 'Programming Language :: Python :: 3.6'],
    zip_safe=True,
)
