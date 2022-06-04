# ScDeepTools
The software includes three deep generative models, a pseudo-cell inference model, a noisy cell inference model, and an LDA-based inference model for cell classification and class-specific genes analysis. Moreover, the software includes an interactive single-cell sequencing cell distribution mapping tool for manipulation of cell deletion and export.

```
unzip ScDeepTools-main.zip
cd ScDeepTools-main
pip install .
```

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

```
$ Impurity_Inference --data ~/data.csv --tags ~/tags.csv --num_epochs 50 --save --save_path ~/output
```

```
$ ******Start data import and gene screening******  
$ ******The gene screening result is as follows:******  
$ Cell number: 13710  
$ Screened gene number: 2441  
$ The labels summary and re-assignment index mapping are as follows:  
                                               cell_number  map_index  
ATTGGGAGGCTTTCGTACCGCTGCCGCCACCAGGTGATACCCGCT         1675          0  
TGTCTACGTCGGACCGCAAGAAGTGAGTCAGAGGCTGCACGCTGT         1226          1  
GCAGCCGGCGTCGTACGAGGCACAGCGGAGACTAGATGAGGCCCC         1470          2  
TTACCCGCAGGAAGACGTATACCCCTCGTGCCAGGCGACCAATGC          621          3  
CTCCCTGGTGTTCAATACCCGATGTGGTGGGCAGAATGTGGCTGG         1363          4  
GTGATCCGCGCAGGCACACATACCGACTCAGATGGGTTGTCCAGG         2176          5  
TGGATGGGATAAGTGCGTGATGGACCGAAGGGACCTCGTGGCCGG         2689          6  
CCCCACCAGGTTGCTTTGTCGGACGAGCCCGCACAGCGCTAGGAT         1419          7  
ATTCAAGGGCAGCCGCGTCACGATTGGATACGACTGTTGGACCGG          734          8  
CGGCTCGTGCTGCGTCGTCTCAAGTCCAGAAACTCCGTGTATCCT          337          9  
$ ******Start ImpurityCell inference model optimization******  
$ 100%|████████████████████████████████████████████████████████████████| 50/50 [02:02<00:00,  2.45s/it, epoch_loss=1.69e-01]  
$ ******Model optimization complete!******  
$ ******Start ImpurityCell probability inference******  
$ ******Inference complete!******  
$ The optimized parameters and the inferred ImpurityCell are saved to: ~/output  
```

```
$ Deep_LDA Inference --data ~/data.csv --num_epochs 50 --save --save_path ~/output
```

```
$ ******Start data import and gene screening******
$ ******The gene screening result is as follows:******
$ Cell number: 13710
$ Screened gene number: 2441
$ ******Start Deep-LDA model optimization******
$ 100%|████████████████████████████████████████████████████████████████| 50/50 [01:17<00:00,  1.54s/it, epoch_loss=7.29e+04]
$ ******Model optimization complete!******
$ ******Start Deep-LDA inference******
$ ******Inference complete!******
$ The optimized parameters and the inferred results are saved to: ~/output
```

```
Deep_LDA Transfer_learning --data ~/data.csv --beta ~/gene_frequency.csv --num_epochs 50 --save --save_path ~/output
```

```
******Start data import and intersect genes******
******Start Deep-LDA classifier optimization******
100%|████████████████████████████████████████████████████████████████| 50/50 [01:06<00:00,  1.33s/it, epoch_loss=8.04e+04]
******Model optimization complete!******
******Start class inference******
******Inference complete!******
The optimized parameters and the inferred results are saved to: ~/output
```
