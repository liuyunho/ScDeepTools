# ScDeepTools
The software includes three deep generative models, a pseudo-cell inference model, a noisy cell inference model, and an LDA-based inference model for cell classification and class-specific genes analysis. Moreover, the software includes an interactive single-cell sequencing cell distribution mapping tool for manipulation of cell deletion and export.

```
$ Pseudo_Inference --data ~/data.csv  --num_epochs 50 --save --save_path ~/output
```

```
$ ******Start data import and gene screening******  
$ ******The gene screening result is as follows:******  
$ Cell number: 13710  
$ Screened gene number: 2441  
$ ******Start pseudocell inference model optimization******  
$ 100%|██████████████████████████████████████████████████████████████████| 50/50 [00:10<00:00,  5.20s/it, epoch_loss=8.28e+04]  
$ ******Model optimization complete!******  
$ ******Start pseudocell probability inference******  
$ ******Inference complete!******  
$ The optimized parameters and the inferred pseudocells are saved to: ~/output  
```
