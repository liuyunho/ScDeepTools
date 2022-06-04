# ScDeepTools
The software includes three deep generative models, a pseudo-cell inference model, a noisy cell inference model, and an LDA-based inference model for cell classification and class-specific genes analysis. Moreover, the software includes an interactive single-cell sequencing cell distribution mapping tool for manipulation of cell deletion and export.

## Installation
This library can be downloaded and then installed locally (Part of the code within files has not been uploaded yet, but the library architecture is complete. Currently, it mainly shows the software running process, and a more detailed tutorial site is being prepared to go online).
```
unzip ScDeepTools-main.zip
cd ScDeepTools-main
pip install .
```

## Usage
After the software installed, three functions can be run, Pseudo_Inference for pseudo cell inference, Impurity_Inference for impurity cell inference, and Deep-LDA for cell classification and class-specific gene inference.

### Pseudo cell inference generative model
Pseudo_Inference can be run from the command line. For more parameter description, you can use -h to query.
```
$ Pseudo_Inference --data ~/data.csv  --num_epochs 50 --save --save_path ~/output
```
Screen output during running
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
The output files include:  
- Optimized pyro parameters and neural network parameters: Em_YYYY_WW_MM .save1 and Em_YYYY_WW_MM .save2
- Inferred pseudo cell probability: Pseudo_Probability.csv

### Impurity cell inference generative model
Impurity_Inference can be run from the command line. For more parameter description, you can use -h to query.
```
$ Impurity_Inference --data ~/data.csv --tags ~/tags.csv --num_epochs 50 --save --save_path ~/output
```
Screen output during running
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
The output files include:  
- Optimized pyro parameters and neural network parameters: Im_YYYY_WW_MM .save1 and Im_YYYY_WW_MM .save2
- Inferred pseudo cell probability: Impurity_Probability.csv

### Deep-LDA Model inference
The Inference module of Deep-LDA can be run from the command line. For more parameter description, you can use -h to query.
```
$ Deep_LDA Inference --data ~/data.csv --num_epochs 50 --save --save_path ~/output
```
Screen output during running
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
The output files include:  
- Optimized pyro parameters and neural network parameters: LDA_YYYY_WW_MM .save1 and LDA_YYYY_WW_MM .save2
- Inferred cell initial class and merged class: Cell_Classification.csv
- Class-specific genes: Class_Specific_Gene.csv
- Class-specific genes intersection: Class_Gene_Intersection.csv
- Trained class-gene frequency: Trained_Gene_Frequency.csv

### Deep-LDA Model Transfer learning
The Transfer_learning module of Deep-LDA can be run from the command line. For more parameter description, you can use -h to query.
```
Deep_LDA Transfer_learning --data ~/data.csv --beta ~/gene_frequency.csv --num_epochs 50 --save --save_path ~/output
```
Screen output during running
```
******Start data import and intersect genes******
******Start Deep-LDA classifier optimization******
100%|████████████████████████████████████████████████████████████████| 50/50 [01:06<00:00,  1.33s/it, epoch_loss=8.04e+04]
******Model optimization complete!******
******Start class inference******
******Inference complete!******
The optimized parameters and the inferred results are saved to: ~/output
```
The output files include:  
- Optimized pyro parameters and neural network parameters: TransferLDA_YYYY_WW_MM .save1 and TransferLDA_YYYY_WW_MM .save2
- Inferred cell annotation: Cell_Transferred_Classification.csv
