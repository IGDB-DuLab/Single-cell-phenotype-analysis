# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 17:58:14 2022

@author: dell
"""
import os
import pandas as pd
import numpy as np
from itertools import combinations
import sympy
import random
import scipy
import scipy.spatial

### 1.input the follow files obtain from  "09_position_phenotype.py"
RNAi_relative_cell_position_Qvalue_binary_001 = pd.read_csv(r"C:\Users\dell\Desktop\output_folder\relative_cell_position_phenotype\RNAi_relative_cell_position_Q-value_binary_0.01.txt", sep="\t", index_col=0)
RNAi_relative_cell_position_Qvalue= pd.read_csv(r"C:\Users\dell\Desktop\output_folder\relative_cell_position_phenotype\RNAi_relative_cell_position_Q-value.txt", index_col= 0,header=0,sep='\t')
RNAi_relative_cell_position_Zscore= pd.read_csv(r"C:\Users\dell\Desktop\output_folder\relative_cell_position_phenotype\RNAi_relative_cell_position_Z-score.txt", index_col= 0,header=0,sep='\t')
RNAi_relative_cell_position_RMSD= pd.read_csv(r"C:\Users\dell\Desktop\output_folder\relative_cell_position_phenotype\RNAi_relative_cell_position_RMSD.txt", index_col= 0,header=0,sep='\t')
CTR_relative_cell_position_RMSD_mean= pd.read_csv(r"C:\Users\dell\Desktop\output_folder\relative_cell_position_phenotype\CTR_relative_cell_position_RMSD_mean.txt", index_col= 0,header=0,sep='\t')
RNAi_XYZ_folder=(r"C:\Users\dell\Desktop\output_folder\RNAi_XYZ")

### 2.input the RNAi embryo length file from “03_distance_matrix.py”
RNAi_embryo_length = pd.read_csv(r'C:\Users\dell\Desktop\output_folder\RNAi_embryo_length.txt', index_col=0, sep='\t')

### 3.input the path of distance matrix of control from “03_distance_matrix.py”
Control_distance_matrix=(r"C:\Users\dell\Desktop\output_folder\Control_distance_matrix")

### 4.assign the output folder path
Output_Folder = r'C:\Users\dell\Desktop\output_folder\cell position correction and simulation'  
if not os.path.exists(Output_Folder):
    os.makedirs(Output_Folder)

#### 5.input the file name of cell position correction file
output_real_and_simulation_position_correction="position_correction_rate_and_simulation"

#############################################################################

################################functions
dict_cell_name = {'ABarpaapaa':'L001100100',	'ABarpaapap':'L001100101',	'ABarpaappa':'L001100110',	'ABarpaappp':'L001100111',	'ABarpapapa':'L001101010',	'ABarpapapp':'L001101011',	'ABarpappaa':'L001101100',	'ABarpappap':'L001101101',	'ABarpapppa':'L001101110',	'ABarppaaaa':'L001110000',	'ABarppaapa':'L001110010',	'ABarpppaaa':'L001111000',	'ABarpppapa':'L001111010',	'ABplaaaapa':'L010000010',	'ABplaaaapp':'L010000011',	'ABplaaapaa':'L010000100',	'ABplaaapap':'L010000101',	'ABplaaappa':'L010000110',	'ABplaappaa':'L010001100',	'ABplaappap':'L010001101',	'ABplaapppa':'L010001110',	'ABplaapppp':'L010001111',	'ABplappppa':'L010011110',	'ABpraappaa':'L011001100',	'ABpraappap':'L011001101',	'ABpraapppa':'L011001110',	'ABpraapppp':'L011001111',	'ABprappppa':'L011011110',	'ABalaaaalpp':'L0000000011',	'ABalaaapall':'L0000001000',	'ABalaaaparr':'L0000001011',	'ABalaaappll':'L0000001100',	'ABalaaapprr':'L0000001111',	'ABalaapaapp':'L0000010011',	'ABalaapappp':'L0000010111',	'ABalaappapp':'L0000011011',	'ABalapaaapp':'L0000100011',	'ABalapapppp':'L0000101111',	'ABalappappp':'L0000110111',	'ABalapppppp':'L0000111111',	'ABalpaaaaaa':'L0001000000',	'ABalpaaaaap':'L0001000001',	'ABalpaaaapa':'L0001000010',	'ABalpaaapaa':'L0001000100',	'ABalpaapaaa':'L0001001000',	'ABalpaapaap':'L0001001001',	'ABalpaapapa':'L0001001010',	'ABalpaapapp':'L0001001011',	'ABalpaappaa':'L0001001100',	'ABalpaappap':'L0001001101',	'ABalpaapppa':'L0001001110',	'ABalpaapppp':'L0001001111',	'ABalpapaaap':'L0001010001',	'ABalpapaapa':'L0001010010',	'ABalpappapa':'L0001011010',	'ABalpappapp':'L0001011011',	'ABalpappppa':'L0001011110',	'ABalpappppp':'L0001011111',	'ABalppaaapp':'L0001100011',	'ABalppaappp':'L0001100111',	'ABalppapaap':'L0001101001',	'ABalppapapp':'L0001101011',	'ABalpppaaap':'L0001110001',	'ABalpppaapd':'L0001110010',	'ABaraaaaaaa':'L0010000000',	'ABaraaaaaap':'L0010000001',	'ABaraaaaapa':'L0010000010',	'ABaraaaaapp':'L0010000011',	'ABaraaaapap':'L0010000101',	'ABaraaapaaa':'L0010001000',	'ABaraaapaap':'L0010001001',	'ABaraaapapa':'L0010001010',	'ABaraaapapp':'L0010001011',	'ABaraaappaa':'L0010001100',	'ABaraaappap':'L0010001101',	'ABaraaapppa':'L0010001110',	'ABaraaapppp':'L0010001111',	'ABaraapaaaa':'L0010010000',	'ABaraapaaap':'L0010010001',	'ABaraapaapa':'L0010010010',	'ABaraapaapp':'L0010010011',	'ABaraapapap':'L0010010101',	'ABaraappaap':'L0010011001',	'ABaraappapa':'L0010011010',	'ABaraappapp':'L0010011011',	'ABaraapppap':'L0010011101',	'ABarapaaaaa':'L0010100000',	'ABarapaaaap':'L0010100001',	'ABarapaaapa':'L0010100010',	'ABarapaapaa':'L0010100100',	'ABarapaappa':'L0010100110',	'ABarapapapa':'L0010101010',	'ABarapapppa':'L0010101110',	'ABarapapppp':'L0010101111',	'ABarappaapa':'L0010110010',	'ABarapppaap':'L0010111001',	'ABarapppapp':'L0010111011',	'ABarpaaaaal':'L0011000000',	'ABarpaaaaar':'L0011000001',	'ABarpaaaapa':'L0011000010',	'ABarpaaaapp':'L0011000011',	'ABarpaaapaa':'L0011000100',	'ABarpaaapap':'L0011000101',	'ABplaapaaaa':'L0100010000',	'ABplaapaaap':'L0100010001',	'ABplaapaapp':'L0100010011',	'ABplpaaaapa':'L0101000010',	'ABplpaaapap':'L0101000101',	'ABplpaapapa':'L0101001010',	'ABplpapapaa':'L0101010100',	'ABplpappaap':'L0101011001',	'ABplpapppap':'L0101011101',	'ABplpappppp':'L0101011111',	'ABplpppapaa':'L0101110100',	'ABplpppapap':'L0101110101',	'ABplppppaap':'L0101111001',	'ABplppppapa':'L0101111010',	'ABplppppapp':'L0101111011',	'ABplpppppaa':'L0101111100',	'ABplpppppap':'L0101111101',	'ABplppppppp':'L0101111111',	'ABpraaaaaap':'L0110000001',	'ABpraaaaapd':'L0110000010',	'ABpraapaaaa':'L0110010000',	'ABpraapaaap':'L0110010001',	'ABpraapaapp':'L0110010011',	'ABprpaaapap':'L0111000101',	'ABprpaapapa':'L0111001010',	'ABprpapapaa':'L0111010100',	'ABprpappppa':'L0111011110',	'ABprpappppp':'L0111011111',	'ABprpppapaa':'L0111110100',	'ABprpppapap':'L0111110101',	'ABprppppaap':'L0111111001',	'ABprppppapa':'L0111111010',	'ABprpppppaa':'L0111111100',	'ABprpppppap':'L0111111101',	'ABprppppppp':'L0111111111',	'ABaraapapaav':'L00100101001',	'ABaraapppaav':'L00100111001',	'ABalaapapa':'L000001010',	'ABalaappaa':'L000001100',	'ABalapapaa':'L000010100',	'ABalappaaa':'L000011000',	'ABalppaaaa':'L000110000',	'ABalppaapa':'L000110010',	'ABaraaaapp':'L001000011',	'ABarpaaapp':'L001100011',	'ABarpapppp':'L001101111',	'ABarppaaap':'L001110001',	'ABarppapaa':'L001110100',	'ABarppapap':'L001110101',	'ABarppappa':'L001110110',	'ABarppappp':'L001110111',	'ABarpppaap':'L001111001',	'ABarppppaa':'L001111100',	'ABarppppap':'L001111101',	'ABarpppppa':'L001111110',	'ABarpppppp':'L001111111',	'ABplaaappp':'L010000111',	'ABplapaapa':'L010010010',	'ABplapaapp':'L010010011',	'ABplapapap':'L010010101',	'ABplapappa':'L010010110',	'ABplappaaa':'L010011000',	'ABplappaap':'L010011001',	'ABplappapa':'L010011010',	'ABplappapp':'L010011011',	'ABplappppp':'L010011111',	'ABplpappap':'L010101101',	'ABplppaaap':'L010110001',	'ABplpppapp':'L010111011',	'ABprapaapa':'L011010010',	'ABprapaapp':'L011010011',	'ABprapapap':'L011010101',	'ABprapappa':'L011010110',	'ABprappaaa':'L011011000',	'ABprappaap':'L011011001',	'ABprappapa':'L011011010',	'ABprappapp':'L011011011',	'ABprappppp':'L011011111',	'ABprppaaap':'L011110001',	'ABprpppapp':'L011111011',	'ABalaaaalal':'L0000000000',	'ABalaaaalar':'L0000000001',	'ABalaaaalpa':'L0000000010',	'ABalaaaarla':'L0000000100',	'ABalaaaarlp':'L0000000101',	'ABalaaaarra':'L0000000110',	'ABalaaaarrp':'L0000000111',	'ABalaaapalr':'L0000001001',	'ABalaaaparl':'L0000001010',	'ABalaaapplr':'L0000001101',	'ABalaaapprl':'L0000001110',	'ABalaapaaal':'L0000010000',	'ABalaapaaar':'L0000010001',	'ABalaapaapa':'L0000010010',	'ABalaapappa':'L0000010110',	'ABalaappapa':'L0000011010',	'ABalaapppaa':'L0000011100',	'ABalaapppap':'L0000011101',	'ABalaappppp':'L0000011111',	'ABalapaaaaa':'L0000100000',	'ABalapaaaap':'L0000100001',	'ABalapaaapa':'L0000100010',	'ABalapaapaa':'L0000100100',	'ABalapaapap':'L0000100101',	'ABalapaappp':'L0000100111',	'ABalapapapp':'L0000101011',	'ABalapappap':'L0000101101',	'ABalapapppa':'L0000101110',	'ABalappaapa':'L0000110010',	'ABalappaapp':'L0000110011',	'ABalappapaa':'L0000110100',	'ABalappapap':'L0000110101',	'ABalappappa':'L0000110110',	'ABalapppaaa':'L0000111000',	'ABalapppaap':'L0000111001',	'ABalapppapp':'L0000111011',	'ABalappppap':'L0000111101',	'ABalapppppa':'L0000111110',	'ABalpaaaapp':'L0001000011',	'ABalpaaapap':'L0001000101',	'ABalpaaappa':'L0001000110',	'ABalpaaappp':'L0001000111',	'ABalpapaaaa':'L0001010000',	'ABalpapaapp':'L0001010011',	'ABalpapapaa':'L0001010100',	'ABalpapappa':'L0001010110',	'ABalpapappp':'L0001010111',	'ABalpappaaa':'L0001011000',	'ABalpapppaa':'L0001011100',	'ABalpapppap':'L0001011101',	'ABalppaaapa':'L0001100010',	'ABalppaappa':'L0001100110',	'ABalppapaaa':'L0001101000',	'ABalppapapa':'L0001101010',	'ABalppappaa':'L0001101100',	'ABalppappap':'L0001101101',	'ABalppapppp':'L0001101111',	'ABalpppaaaa':'L0001110000',	'ABalpppaapv':'L0001110011',	'ABalpppapad':'L0001110100',	'ABalpppapav':'L0001110101',	'ABalpppappa':'L0001110110',	'ABalppppaad':'L0001111000',	'ABalppppaav':'L0001111001',	'ABalppppapp':'L0001111011',	'ABalpppppaa':'L0001111100',	'ABalpppppap':'L0001111101',	'ABaraaaapaa':'L0010000100',	'ABaraapappa':'L0010010110',	'ABaraapappp':'L0010010111',	'ABaraappaaa':'L0010011000',	'ABaraappppa':'L0010011110',	'ABaraappppp':'L0010011111',	'ABarapaaapp':'L0010100011',	'ABarapaapap':'L0010100101',	'ABarapaappp':'L0010100111',	'ABarapapaaa':'L0010101000',	'ABarapapapp':'L0010101011',	'ABarapappaa':'L0010101100',	'ABarapappap':'L0010101101',	'ABarappaaaa':'L0010110000',	'ABarappaaap':'L0010110001',	'ABarappaapp':'L0010110011',	'ABarappapaa':'L0010110100',	'ABarappappa':'L0010110110',	'ABarappappp':'L0010110111',	'ABarapppaaa':'L0010111000',	'ABarapppapa':'L0010111010',	'ABarappppaa':'L0010111100',	'ABarappppap':'L0010111101',	'ABarapppppp':'L0010111111',	'ABarpapaaaa':'L0011010000',	'ABarpapaaap':'L0011010001',	'ABarpapaapa':'L0011010010',	'ABarppaappa':'L0011100110',	'ABarppaappp':'L0011100111',	'ABarpppappa':'L0011110110',	'ABarpppappp':'L0011110111',	'ABplaaaaaaa':'L0100000000',	'ABplaaaaaap':'L0100000001',	'ABplaaaaapa':'L0100000010',	'ABplaapaapa':'L0100010010',	'ABplaapapaa':'L0100010100',	'ABplaapapap':'L0100010101',	'ABplaapappa':'L0100010110',	'ABplapaaaaa':'L0100100000',	'ABplapaaapp':'L0100100011',	'ABplapapaaa':'L0100101000',	'ABplapapaap':'L0100101001',	'ABplapapppa':'L0100101110',	'ABplapppaaa':'L0100111000',	'ABplapppaap':'L0100111001',	'ABplapppapa':'L0100111010',	'ABplpaaaaaa':'L0101000000',	'ABplpaaaaap':'L0101000001',	'ABplpaaaapp':'L0101000011',	'ABplpaaapaa':'L0101000100',	'ABplpaaappp':'L0101000111',	'ABplpaapaaa':'L0101001000',	'ABplpaapaap':'L0101001001',	'ABplpaapapp':'L0101001011',	'ABplpaappaa':'L0101001100',	'ABplpaappap':'L0101001101',	'ABplpaapppa':'L0101001110',	'ABplpapaaaa':'L0101010000',	'ABplpapaaap':'L0101010001',	'ABplpapaapa':'L0101010010',	'ABplpapaapp':'L0101010011',	'ABplpapapap':'L0101010101',	'ABplpapappa':'L0101010110',	'ABplpapappp':'L0101010111',	'ABplpappaaa':'L0101011000',	'ABplpapppaa':'L0101011100',	'ABplpappppa':'L0101011110',	'ABplppaaaaa':'L0101100000',	'ABplppaapaa':'L0101100100',	'ABplppaapap':'L0101100101',	'ABplppaappa':'L0101100110',	'ABplppaappp':'L0101100111',	'ABplppapaap':'L0101101001',	'ABplppapapa':'L0101101010',	'ABplppapapp':'L0101101011',	'ABplppappaa':'L0101101100',	'ABplppappap':'L0101101101',	'ABplppapppa':'L0101101110',	'ABplppapppp':'L0101101111',	'ABplpppaaaa':'L0101110000',	'ABplpppaaap':'L0101110001',	'ABplpppaapp':'L0101110011',	'ABplppppaaa':'L0101111000',	'ABplppppppa':'L0101111110',	'ABpraaaaaaa':'L0110000000',	'ABpraaaaapv':'L0110000011',	'ABpraaaapad':'L0110000100',	'ABpraaaapav':'L0110000101',	'ABpraaaappa':'L0110000110',	'ABpraaapaad':'L0110001000',	'ABpraaapaav':'L0110001001',	'ABpraaapapp':'L0110001011',	'ABpraaappaa':'L0110001100',	'ABpraaappap':'L0110001101',	'ABpraapaapa':'L0110010010',	'ABpraapapaa':'L0110010100',	'ABpraapapap':'L0110010101',	'ABpraapappa':'L0110010110',	'ABprapaaaaa':'L0110100000',	'ABprapaaapp':'L0110100011',	'ABprapapaaa':'L0110101000',	'ABprapapaap':'L0110101001',	'ABprapapppa':'L0110101110',	'ABprapppaaa':'L0110111000',	'ABprapppaap':'L0110111001',	'ABprapppapa':'L0110111010',	'ABprpaaaaaa':'L0111000000',	'ABprpaaaaap':'L0111000001',	'ABprpaaaapa':'L0111000010',	'ABprpaaaapp':'L0111000011',	'ABprpaaapaa':'L0111000100',	'ABprpaaappp':'L0111000111',	'ABprpaapaaa':'L0111001000',	'ABprpaapaap':'L0111001001',	'ABprpaapapp':'L0111001011',	'ABprpaappaa':'L0111001100',	'ABprpaappap':'L0111001101',	'ABprpaapppa':'L0111001110',	'ABprpapaaaa':'L0111010000',	'ABprpapaaap':'L0111010001',	'ABprpapaapa':'L0111010010',	'ABprpapaapp':'L0111010011',	'ABprpapapap':'L0111010101',	'ABprpapappa':'L0111010110',	'ABprpapappp':'L0111010111',	'ABprpappaaa':'L0111011000',	'ABprpappaap':'L0111011001',	'ABprpappapa':'L0111011010',	'ABprpappapp':'L0111011011',	'ABprpapppaa':'L0111011100',	'ABprpapppap':'L0111011101',	'ABprppaaaaa':'L0111100000',	'ABprppaapaa':'L0111100100',	'ABprppaapap':'L0111100101',	'ABprppaappa':'L0111100110',	'ABprppaappp':'L0111100111',	'ABprppapaap':'L0111101001',	'ABprppapapa':'L0111101010',	'ABprppapapp':'L0111101011',	'ABprppappaa':'L0111101100',	'ABprppappap':'L0111101101',	'ABprppapppa':'L0111101110',	'ABprppapppp':'L0111101111',	'ABprpppaaaa':'L0111110000',	'ABprpppaaap':'L0111110001',	'ABprpppaapp':'L0111110011',	'ABprppppaaa':'L0111111000',	'ABprppppapp':'L0111111011',	'ABprppppppa':'L0111111110',	'ABalaappppaa':'L00000111100',	'ABalaappppap':'L00000111101',	'ABalapaappaa':'L00001001100',	'ABalapaappap':'L00001001101',	'ABalapapapaa':'L00001010100',	'ABalapapapap':'L00001010101',	'ABalapappaaa':'L00001011000',	'ABalapappaap':'L00001011001',	'ABalapppapaa':'L00001110100',	'ABalapppapap':'L00001110101',	'ABalappppaaa':'L00001111000',	'ABalappppaap':'L00001111001',	'ABalpapapapa':'L00010101010',	'ABalpapapapp':'L00010101011',	'ABalpappaapa':'L00010110010',	'ABalpappaapp':'L00010110011',	'ABalppapppaa':'L00011011100',	'ABalppapppap':'L00011011101',	'ABalpppapppa':'L00011101110',	'ABalpppapppp':'L00011101111',	'ABalppppapaa':'L00011110100',	'ABalppppapap':'L00011110101',	'ABalppppppaa':'L00011111100',	'ABalppppppap':'L00011111101',	'ABalpppppppa':'L00011111110',	'ABalpppppppp':'L00011111111',	'ABaraapapaad':'L00100101000',	'ABaraapppaad':'L00100111000',	'ABarapapaapa':'L00101010010',	'ABarapapaapp':'L00101010011',	'ABarappapapa':'L00101101010',	'ABarappapapp':'L00101101011',	'ABarapppppaa':'L00101111100',	'ABarapppppap':'L00101111101',	'ABarpapaappa':'L00110100110',	'ABarpapaappp':'L00110100111',	'ABplaaaaappa':'L01000000110',	'ABplaaaaappp':'L01000000111',	'ABplaapapppa':'L01000101110',	'ABplaapapppp':'L01000101111',	'ABplapaaaapa':'L01001000010',	'ABplapaaaapp':'L01001000011',	'ABplapaaapad':'L01001000100',	'ABplapaaapav':'L01001000101',	'ABplapappppp':'L01001011111',	'ABplapppappa':'L01001110110',	'ABplapppappp':'L01001110111',	'ABplpaaappaa':'L01010001100',	'ABplpaaappap':'L01010001101',	'ABplpaappppa':'L01010011110',	'ABplpaappppp':'L01010011111',	'ABplppaaaapa':'L01011000010',	'ABplppaaaapp':'L01011000011',	'ABplppapaaaa':'L01011010000',	'ABplppapaaap':'L01011010001',	'ABplpppaapaa':'L01011100100',	'ABplpppaapap':'L01011100101',	'ABpraaaapppa':'L01100001110',	'ABpraaaapppp':'L01100001111',	'ABpraaapapaa':'L01100010100',	'ABpraaapapap':'L01100010101',	'ABpraaapppaa':'L01100011100',	'ABpraaapppap':'L01100011101',	'ABpraaappppa':'L01100011110',	'ABpraaappppp':'L01100011111',	'ABpraapapppa':'L01100101110',	'ABpraapapppp':'L01100101111',	'ABprapaaaapa':'L01101000010',	'ABprapaaaapp':'L01101000011',	'ABprapaaapad':'L01101000100',	'ABprapaaapav':'L01101000101',	'ABprapappppp':'L01101011111',	'ABprapppappa':'L01101110110',	'ABprapppappp':'L01101110111',	'ABprpaaappaa':'L01110001100',	'ABprpaaappap':'L01110001101',	'ABprpaappppa':'L01110011110',	'ABprpaappppp':'L01110011111',	'ABprppaaaapa':'L01111000010',	'ABprppaaaapp':'L01111000011',	'ABprppapaaaa':'L01111010000',	'ABprppapaaap':'L01111010001',	'ABprpppaapaa':'L01111100100',	'ABprpppaapap':'L01111100101',	'ABplapappppaa':'L010010111100',	'ABplapappppap':'L010010111101',	'ABprapappppaa':'L011010111100',	'ABprapappppap':'L011010111101',	'AB':'L0',	'ABa':'L00',	'ABp':'L01',	'ABal':'L000',	'ABar':'L001',	'ABpl':'L010',	'ABpr':'L011',	'ABala':'L0000',	'ABalp':'L0001',	'ABara':'L0010',	'ABarp':'L0011',	'ABpla':'L0100',	'ABplp':'L0101',	'ABpra':'L0110',	'ABprp':'L0111',	'ABalaa':'L00000',	'ABalap':'L00001',	'ABalpa':'L00010',	'ABalpp':'L00011',	'ABaraa':'L00100',	'ABarap':'L00101',	'ABarpa':'L00110',	'ABarpp':'L00111',	'ABplaa':'L01000',	'ABplap':'L01001',	'ABplpa':'L01010',	'ABplpp':'L01011',	'ABpraa':'L01100',	'ABprap':'L01101',	'ABprpa':'L01110',	'ABprpp':'L01111',	'ABalaaa':'L000000',	'ABalaap':'L000001',	'ABalapa':'L000010',	'ABalapp':'L000011',	'ABalpaa':'L000100',	'ABalpap':'L000101',	'ABalppa':'L000110',	'ABalppp':'L000111',	'ABaraaa':'L001000',	'ABaraap':'L001001',	'ABarapa':'L001010',	'ABarapp':'L001011',	'ABarpaa':'L001100',	'ABarpap':'L001101',	'ABarppa':'L001110',	'ABarppp':'L001111',	'ABplaaa':'L010000',	'ABplaap':'L010001',	'ABplapa':'L010010',	'ABplapp':'L010011',	'ABplpaa':'L010100',	'ABplpap':'L010101',	'ABplppa':'L010110',	'ABplppp':'L010111',	'ABpraaa':'L011000',	'ABpraap':'L011001',	'ABprapa':'L011010',	'ABprapp':'L011011',	'ABprpaa':'L011100',	'ABprpap':'L011101',	'ABprppa':'L011110',	'ABprppp':'L011111',	'ABalaaaa':'L0000000',	'ABalaaap':'L0000001',	'ABalaapa':'L0000010',	'ABalaapp':'L0000011',	'ABalapaa':'L0000100',	'ABalapap':'L0000101',	'ABalappa':'L0000110',	'ABalappp':'L0000111',	'ABalpaaa':'L0001000',	'ABalpaap':'L0001001',	'ABalpapa':'L0001010',	'ABalpapp':'L0001011',	'ABalppaa':'L0001100',	'ABalppap':'L0001101',	'ABalpppa':'L0001110',	'ABalpppp':'L0001111',	'ABaraaaa':'L0010000',	'ABaraaap':'L0010001',	'ABaraapa':'L0010010',	'ABaraapp':'L0010011',	'ABarapaa':'L0010100',	'ABarapap':'L0010101',	'ABarappa':'L0010110',	'ABarappp':'L0010111',	'ABarpaaa':'L0011000',	'ABarpaap':'L0011001',	'ABarpapa':'L0011010',	'ABarpapp':'L0011011',	'ABarppaa':'L0011100',	'ABarppap':'L0011101',	'ABarpppa':'L0011110',	'ABarpppp':'L0011111',	'ABplaaaa':'L0100000',	'ABplaaap':'L0100001',	'ABplaapa':'L0100010',	'ABplaapp':'L0100011',	'ABplapaa':'L0100100',	'ABplapap':'L0100101',	'ABplappa':'L0100110',	'ABplappp':'L0100111',	'ABplpaaa':'L0101000',	'ABplpaap':'L0101001',	'ABplpapa':'L0101010',	'ABplpapp':'L0101011',	'ABplppaa':'L0101100',	'ABplppap':'L0101101',	'ABplpppa':'L0101110',	'ABplpppp':'L0101111',	'ABpraaaa':'L0110000',	'ABpraaap':'L0110001',	'ABpraapa':'L0110010',	'ABpraapp':'L0110011',	'ABprapaa':'L0110100',	'ABprapap':'L0110101',	'ABprappa':'L0110110',	'ABprappp':'L0110111',	'ABprpaaa':'L0111000',	'ABprpaap':'L0111001',	'ABprpapa':'L0111010',	'ABprpapp':'L0111011',	'ABprppaa':'L0111100',	'ABprppap':'L0111101',	'ABprpppa':'L0111110',	'ABprpppp':'L0111111',	'ABalaaaal':'L00000000',	'ABalaaaar':'L00000001',	'ABalaaapa':'L00000010',	'ABalaaapp':'L00000011',	'ABalaapaa':'L00000100',	'ABalaapap':'L00000101',	'ABalaappa':'L00000110',	'ABalaappp':'L00000111',	'ABalapaaa':'L00001000',	'ABalapaap':'L00001001',	'ABalapapa':'L00001010',	'ABalapapp':'L00001011',	'ABalappaa':'L00001100',	'ABalappap':'L00001101',	'ABalapppa':'L00001110',	'ABalapppp':'L00001111',	'ABalpaaaa':'L00010000',	'ABalpaaap':'L00010001',	'ABalpaapa':'L00010010',	'ABalpaapp':'L00010011',	'ABalpapaa':'L00010100',	'ABalpapap':'L00010101',	'ABalpappa':'L00010110',	'ABalpappp':'L00010111',	'ABalppaaa':'L00011000',	'ABalppaap':'L00011001',	'ABalppapa':'L00011010',	'ABalppapp':'L00011011',	'ABalpppaa':'L00011100',	'ABalpppap':'L00011101',	'ABalppppa':'L00011110',	'ABalppppp':'L00011111',	'ABaraaaaa':'L00100000',	'ABaraaaap':'L00100001',	'ABaraaapa':'L00100010',	'ABaraaapp':'L00100011',	'ABaraapaa':'L00100100',	'ABaraapap':'L00100101',	'ABaraappa':'L00100110',	'ABaraappp':'L00100111',	'ABarapaaa':'L00101000',	'ABarapaap':'L00101001',	'ABarapapa':'L00101010',	'ABarapapp':'L00101011',	'ABarappaa':'L00101100',	'ABarappap':'L00101101',	'ABarapppa':'L00101110',	'ABarapppp':'L00101111',	'ABarpaaaa':'L00110000',	'ABarpaaap':'L00110001',	'ABarpaapa':'L00110010',	'ABarpaapp':'L00110011',	'ABarpapaa':'L00110100',	'ABarpapap':'L00110101',	'ABarpappa':'L00110110',	'ABarpappp':'L00110111',	'ABarppaaa':'L00111000',	'ABarppaap':'L00111001',	'ABarppapa':'L00111010',	'ABarppapp':'L00111011',	'ABarpppaa':'L00111100',	'ABarpppap':'L00111101',	'ABarppppa':'L00111110',	'ABarppppp':'L00111111',	'ABplaaaaa':'L01000000',	'ABplaaaap':'L01000001',	'ABplaaapa':'L01000010',	'ABplaaapp':'L01000011',	'ABplaapaa':'L01000100',	'ABplaapap':'L01000101',	'ABplaappa':'L01000110',	'ABplaappp':'L01000111',	'ABplapaaa':'L01001000',	'ABplapaap':'L01001001',	'ABplapapa':'L01001010',	'ABplapapp':'L01001011',	'ABplappaa':'L01001100',	'ABplappap':'L01001101',	'ABplapppa':'L01001110',	'ABplapppp':'L01001111',	'ABplpaaaa':'L01010000',	'ABplpaaap':'L01010001',	'ABplpaapa':'L01010010',	'ABplpaapp':'L01010011',	'ABplpapaa':'L01010100',	'ABplpapap':'L01010101',	'ABplpappa':'L01010110',	'ABplpappp':'L01010111',	'ABplppaaa':'L01011000',	'ABplppaap':'L01011001',	'ABplppapa':'L01011010',	'ABplppapp':'L01011011',	'ABplpppaa':'L01011100',	'ABplpppap':'L01011101',	'ABplppppa':'L01011110',	'ABplppppp':'L01011111',	'ABpraaaaa':'L01100000',	'ABpraaaap':'L01100001',	'ABpraaapa':'L01100010',	'ABpraaapp':'L01100011',	'ABpraapaa':'L01100100',	'ABpraapap':'L01100101',	'ABpraappa':'L01100110',	'ABpraappp':'L01100111',	'ABprapaaa':'L01101000',	'ABprapaap':'L01101001',	'ABprapapa':'L01101010',	'ABprapapp':'L01101011',	'ABprappaa':'L01101100',	'ABprappap':'L01101101',	'ABprapppa':'L01101110',	'ABprapppp':'L01101111',	'ABprpaaaa':'L01110000',	'ABprpaaap':'L01110001',	'ABprpaapa':'L01110010',	'ABprpaapp':'L01110011',	'ABprpapaa':'L01110100',	'ABprpapap':'L01110101',	'ABprpappa':'L01110110',	'ABprpappp':'L01110111',	'ABprppaaa':'L01111000',	'ABprppaap':'L01111001',	'ABprppapa':'L01111010',	'ABprppapp':'L01111011',	'ABprpppaa':'L01111100',	'ABprpppap':'L01111101',	'ABprppppa':'L01111110',	'ABprppppp':'L01111111',	'ABalaaaala':'L000000000',	'ABalaaaalp':'L000000001',	'ABalaaaarl':'L000000010',	'ABalaaaarr':'L000000011',	'ABalaaapal':'L000000100',	'ABalaaapar':'L000000101',	'ABalaaappl':'L000000110',	'ABalaaappr':'L000000111',	'ABalaapaaa':'L000001000',	'ABalaapaap':'L000001001',	'ABalaapapp':'L000001011',	'ABalaappap':'L000001101',	'ABalaapppa':'L000001110',	'ABalaapppp':'L000001111',	'ABalapaaaa':'L000010000',	'ABalapaaap':'L000010001',	'ABalapaapa':'L000010010',	'ABalapaapp':'L000010011',	'ABalapapap':'L000010101',	'ABalapappa':'L000010110',	'ABalapappp':'L000010111',	'ABalappaap':'L000011001',	'ABalappapa':'L000011010',	'ABalappapp':'L000011011',	'ABalapppaa':'L000011100',	'ABalapppap':'L000011101',	'ABalappppa':'L000011110',	'ABalappppp':'L000011111',	'ABalpaaaaa':'L000100000',	'ABalpaaaap':'L000100001',	'ABalpaaapa':'L000100010',	'ABalpaaapp':'L000100011',	'ABalpaapaa':'L000100100',	'ABalpaapap':'L000100101',	'ABalpaappa':'L000100110',	'ABalpaappp':'L000100111',	'ABalpapaaa':'L000101000',	'ABalpapaap':'L000101001',	'ABalpapapa':'L000101010',	'ABalpapapp':'L000101011',	'ABalpappaa':'L000101100',	'ABalpappap':'L000101101',	'ABalpapppa':'L000101110',	'ABalpapppp':'L000101111',	'ABalppaaap':'L000110001',	'ABalppaapp':'L000110011',	'ABalppapaa':'L000110100',	'ABalppapap':'L000110101',	'ABalppappa':'L000110110',	'ABalppappp':'L000110111',	'ABalpppaaa':'L000111000',	'ABalpppaap':'L000111001',	'ABalpppapa':'L000111010',	'ABalpppapp':'L000111011',	'ABalppppaa':'L000111100',	'ABalppppap':'L000111101',	'ABalpppppa':'L000111110',	'ABalpppppp':'L000111111',	'ABaraaaaaa':'L001000000',	'ABaraaaaap':'L001000001',	'ABaraaaapa':'L001000010',	'ABaraaapaa':'L001000100',	'ABaraaapap':'L001000101',	'ABaraaappa':'L001000110',	'ABaraaappp':'L001000111',	'ABaraapaaa':'L001001000',	'ABaraapaap':'L001001001',	'ABaraapapa':'L001001010',	'ABaraapapp':'L001001011',	'ABaraappaa':'L001001100',	'ABaraappap':'L001001101',	'ABaraapppa':'L001001110',	'ABaraapppp':'L001001111',	'ABarapaaaa':'L001010000',	'ABarapaaap':'L001010001',	'ABarapaapa':'L001010010',	'ABarapaapp':'L001010011',	'ABarapapaa':'L001010100',	'ABarapapap':'L001010101',	'ABarapappa':'L001010110',	'ABarapappp':'L001010111',	'ABarappaaa':'L001011000',	'ABarappaap':'L001011001',	'ABarappapa':'L001011010',	'ABarappapp':'L001011011',	'ABarapppaa':'L001011100',	'ABarapppap':'L001011101',	'ABarappppa':'L001011110',	'ABarappppp':'L001011111',	'ABarpaaaaa':'L001100000',	'ABarpaaaap':'L001100001',	'ABarpaaapa':'L001100010',	'ABarpapaaa':'L001101000',	'ABarpapaap':'L001101001',	'ABarppaapp':'L001110011',	'ABarpppapp':'L001111011',	'ABplaaaaaa':'L010000000',	'ABplaaaaap':'L010000001',	'ABplaapaaa':'L010001000',	'ABplaapaap':'L010001001',	'ABplaapapa':'L010001010',	'ABplaapapp':'L010001011',	'ABplapaaaa':'L010010000',	'ABplapaaap':'L010010001',	'ABplapapaa':'L010010100',	'ABplapappp':'L010010111',	'ABplapppaa':'L010011100',	'ABplapppap':'L010011101',	'ABplpaaaaa':'L010100000',	'ABplpaaaap':'L010100001',	'ABplpaaapa':'L010100010',	'ABplpaaapp':'L010100011',	'ABplpaapaa':'L010100100',	'ABplpaapap':'L010100101',	'ABplpaappa':'L010100110',	'ABplpaappp':'L010100111',	'ABplpapaaa':'L010101000',	'ABplpapaap':'L010101001',	'ABplpapapa':'L010101010',	'ABplpapapp':'L010101011',	'ABplpappaa':'L010101100',	'ABplpapppa':'L010101110',	'ABplpapppp':'L010101111',	'ABplppaaaa':'L010110000',	'ABplppaapa':'L010110010',	'ABplppaapp':'L010110011',	'ABplppapaa':'L010110100',	'ABplppapap':'L010110101',	'ABplppappa':'L010110110',	'ABplppappp':'L010110111',	'ABplpppaaa':'L010111000',	'ABplpppaap':'L010111001',	'ABplpppapa':'L010111010',	'ABplppppaa':'L010111100',	'ABplppppap':'L010111101',	'ABplpppppa':'L010111110',	'ABplpppppp':'L010111111',	'ABpraaaaaa':'L011000000',	'ABpraaaaap':'L011000001',	'ABpraaaapa':'L011000010',	'ABpraaaapp':'L011000011',	'ABpraaapaa':'L011000100',	'ABpraaapap':'L011000101',	'ABpraaappa':'L011000110',	'ABpraaappp':'L011000111',	'ABpraapaaa':'L011001000',	'ABpraapaap':'L011001001',	'ABpraapapa':'L011001010',	'ABpraapapp':'L011001011',	'ABprapaaaa':'L011010000',	'ABprapaaap':'L011010001',	'ABprapapaa':'L011010100',	'ABprapappp':'L011010111',	'ABprapppaa':'L011011100',	'ABprapppap':'L011011101',	'ABprpaaaaa':'L011100000',	'ABprpaaaap':'L011100001',	'ABprpaaapa':'L011100010',	'ABprpaaapp':'L011100011',	'ABprpaapaa':'L011100100',	'ABprpaapap':'L011100101',	'ABprpaappa':'L011100110',	'ABprpaappp':'L011100111',	'ABprpapaaa':'L011101000',	'ABprpapaap':'L011101001',	'ABprpapapa':'L011101010',	'ABprpapapp':'L011101011',	'ABprpappaa':'L011101100',	'ABprpappap':'L011101101',	'ABprpapppa':'L011101110',	'ABprpapppp':'L011101111',	'ABprppaaaa':'L011110000',	'ABprppaapa':'L011110010',	'ABprppaapp':'L011110011',	'ABprppapaa':'L011110100',	'ABprppapap':'L011110101',	'ABprppappa':'L011110110',	'ABprppappp':'L011110111',	'ABprpppaaa':'L011111000',	'ABprpppaap':'L011111001',	'ABprpppapa':'L011111010',	'ABprppppaa':'L011111100',	'ABprppppap':'L011111101',	'ABprpppppa':'L011111110',	'ABprpppppp':'L011111111',	'ABalaappppa':'L0000011110',	'ABalapaappa':'L0000100110',	'ABalapapapa':'L0000101010',	'ABalapappaa':'L0000101100',	'ABalapppapa':'L0000111010',	'ABalappppaa':'L0000111100',	'ABalpapapap':'L0001010101',	'ABalpappaap':'L0001011001',	'ABalppapppa':'L0001101110',	'ABalpppappp':'L0001110111',	'ABalppppapa':'L0001111010',	'ABalppppppa':'L0001111110',	'ABalppppppp':'L0001111111',	'ABaraapapaa':'L0010010100',	'ABaraapppaa':'L0010011100',	'ABarapapaap':'L0010101001',	'ABarappapap':'L0010110101',	'ABarapppppa':'L0010111110',	'ABarpapaapp':'L0011010011',	'ABplaaaaapp':'L0100000011',	'ABplaapappp':'L0100010111',	'ABplapaaaap':'L0100100001',	'ABplapaaapa':'L0100100010',	'ABplapapppp':'L0100101111',	'ABplapppapp':'L0100111011',	'ABplpaaappa':'L0101000110',	'ABplpaapppp':'L0101001111',	'ABplppaaaap':'L0101100001',	'ABplppapaaa':'L0101101000',	'ABplpppaapa':'L0101110010',	'ABpraaaappp':'L0110000111',	'ABpraaapapa':'L0110001010',	'ABpraaapppa':'L0110001110',	'ABpraaapppp':'L0110001111',	'ABpraapappp':'L0110010111',	'ABprapaaaap':'L0110100001',	'ABprapaaapa':'L0110100010',	'ABprapapppp':'L0110101111',	'ABprapppapp':'L0110111011',	'ABprpaaappa':'L0111000110',	'ABprpaapppp':'L0111001111',	'ABprppaaaap':'L0111100001',	'ABprppapaaa':'L0111101000',	'ABprpppaapa':'L0111110010',	'ABplapappppa':'L01001011110',	'ABprapappppa':'L01101011110',	'Caaaaa':'L11000000',	'Caaaap':'L11000001',	'Caaapa':'L11000010',	'Caaapp':'L11000011',	'Caappd':'L11000110',	'Caappv':'L11000111',	'Cpaaaa':'L11010000',	'Cpaaap':'L11010001',	'Cpaapa':'L11010010',	'Cpaapp':'L11010011',	'Cpapaa':'L11010100',	'Cpapap':'L11010101',	'Cpappd':'L11010110',	'Cpappv':'L11010111',	'Capaaaa':'L110010000',	'Capaaap':'L110010001',	'Capaapa':'L110010010',	'Capaapp':'L110010011',	'Capapaa':'L110010100',	'Capapap':'L110010101',	'Capappa':'L110010110',	'Capappp':'L110010111',	'Cappaaa':'L110011000',	'Cappaap':'L110011001',	'Cappapa':'L110011010',	'Cappapp':'L110011011',	'Capppaa':'L110011100',	'Capppap':'L110011101',	'Cappppd':'L110011110',	'Cappppv':'L110011111',	'Cppaaaa':'L110110000',	'Cppaaap':'L110110001',	'Cppaapa':'L110110010',	'Cppaapp':'L110110011',	'Cppapaa':'L110110100',	'Cppapap':'L110110101',	'Cppappa':'L110110110',	'Cppappp':'L110110111',	'Cpppaaa':'L110111000',	'Cpppaap':'L110111001',	'Cpppapa':'L110111010',	'Cpppapp':'L110111011',	'Cppppaa':'L110111100',	'Cppppap':'L110111101',	'Cpppppd':'L110111110',	'Cpppppv':'L110111111',	'Caapaa':'L11000100',	'Caapap':'L11000101',	'Capaaa':'L11001000',	'Capaap':'L11001001',	'Capapa':'L11001010',	'Capapp':'L11001011',	'Cappaa':'L11001100',	'Cappap':'L11001101',	'Capppa':'L11001110',	'Capppp':'L11001111',	'Cppaaa':'L11011000',	'Cppaap':'L11011001',	'Cppapa':'L11011010',	'Cppapp':'L11011011',	'Cpppaa':'L11011100',	'Cpppap':'L11011101',	'Cppppa':'L11011110',	'Cppppp':'L11011111',	'Caaaa':'L1100000',	'Caaap':'L1100001',	'Caapa':'L1100010',	'Caapp':'L1100011',	'Capaa':'L1100100',	'Capap':'L1100101',	'Cappa':'L1100110',	'Cappp':'L1100111',	'Cpaaa':'L1101000',	'Cpaap':'L1101001',	'Cpapa':'L1101010',	'Cpapp':'L1101011',	'Cppaa':'L1101100',	'Cppap':'L1101101',	'Cpppa':'L1101110',	'Cpppp':'L1101111',	'Caaa':'L110000',	'Caap':'L110001',	'Capa':'L110010',	'Capp':'L110011',	'Cpaa':'L110100',	'Cpap':'L110101',	'Cppa':'L110110',	'Cppp':'L110111',	'Caa':'L11000',	'Cap':'L11001',	'Cpa':'L11010',	'Cpp':'L11011',	'Ca':'L1100',	'Cp':'L1101',	'C':'L110',	'Daaaa':'L11100000',	'Daaap':'L11100001',	'Daapa':'L11100010',	'Daapp':'L11100011',	'Dapaa':'L11100100',	'Dapap':'L11100101',	'Dpaaa':'L11101000',	'Dpaap':'L11101001',	'Dpapa':'L11101010',	'Dpapp':'L11101011',	'Dppaa':'L11101100',	'Dppap':'L11101101',	'Dappaa':'L111001100',	'Dappap':'L111001101',	'Dapppa':'L111001110',	'Dapppp':'L111001111',	'Dpppaa':'L111011100',	'Dpppap':'L111011101',	'Dppppa':'L111011110',	'Dppppp':'L111011111',	'Dappa':'L11100110',	'Dappp':'L11100111',	'Dpppa':'L11101110',	'Dpppp':'L11101111',	'Daaa':'L1110000',	'Daap':'L1110001',	'Dapa':'L1110010',	'Dapp':'L1110011',	'Dpaa':'L1110100',	'Dpap':'L1110101',	'Dppa':'L1110110',	'Dppp':'L1110111',	'Daa':'L111000',	'Dap':'L111001',	'Dpa':'L111010',	'Dpp':'L111011',	'Da':'L11100',	'Dp':'L11101',	'D':'L1110',	'Ealaad':'L10100000',	'Ealaav':'L10100001',	'Ealap':'L1010001',	'Ealpa':'L1010010',	'Ealpp':'L1010011',	'Earaad':'L10101000',	'Earaav':'L10101001',	'Earap':'L1010101',	'Earpa':'L1010110',	'Earpp':'L1010111',	'Eplaa':'L1011000',	'Eplap':'L1011001',	'Eplpa':'L1011010',	'Eplppa':'L10110110',	'Eplppp':'L10110111',	'Epraa':'L1011100',	'Eprap':'L1011101',	'Eprpa':'L1011110',	'Eprppa':'L10111110',	'Eprppp':'L10111111',	'E':'L101',	'Ea':'L1010',	'Eal':'L10100',	'Eala':'L101000',	'Ealaa':'L1010000',	'Ealp':'L101001',	'Ear':'L10101',	'Eara':'L101010',	'Earaa':'L1010100',	'Earp':'L101011',	'Ep':'L1011',	'Epl':'L10110',	'Epla':'L101100',	'Eplp':'L101101',	'Eplpp':'L1011011',	'Epr':'L10111',	'Epra':'L101110',	'Eprp':'L101111',	'Eprpp':'L1011111',	'MSaaappp':'L100000111',	'MSaappaa':'L100001100',	'MSaappap':'L100001101',	'MSapaaap':'L100010001',	'MSapapap':'L100010101',	'MSapappa':'L100010110',	'MSapappp':'L100010111',	'MSappaaa':'L100011000',	'MSappapp':'L100011011',	'MSapppaa':'L100011100',	'MSapppap':'L100011101',	'MSappppa':'L100011110',	'MSappppp':'L100011111',	'MSpappaa':'L100101100',	'MSpappap':'L100101101',	'MSppaaap':'L100110001',	'MSppaapp':'L100110011',	'MSppapap':'L100110101',	'MSppappa':'L100110110',	'MSppappp':'L100110111',	'MSpppapp':'L100111011',	'MSppppaa':'L100111100',	'MSppppap':'L100111101',	'MSpppppa':'L100111110',	'MSpppppp':'L100111111',	'MSaaaaaal':'L1000000000',	'MSaaaaaar':'L1000000001',	'MSaaaaapp':'L1000000011',	'MSaaaapap':'L1000000101',	'MSaaaappp':'L1000000111',	'MSaaapaaa':'L1000001000',	'MSaaapaap':'L1000001001',	'MSaaapapa':'L1000001010',	'MSaaapapp':'L1000001011',	'MSaapaaaa':'L1000010000',	'MSaapaaap':'L1000010001',	'MSaapaapp':'L1000010011',	'MSaapapaa':'L1000010100',	'MSaapappa':'L1000010110',	'MSaapappp':'L1000010111',	'MSaapppaa':'L1000011100',	'MSaapppap':'L1000011101',	'MSaappppa':'L1000011110',	'MSaappppp':'L1000011111',	'MSapaaaad':'L1000100000',	'MSapaaaav':'L1000100001',	'MSapapaaa':'L1000101000',	'MSapapaap':'L1000101001',	'MSpaaaapa':'L1001000010',	'MSpaaaapp':'L1001000011',	'MSpaaappa':'L1001000110',	'MSpaaappp':'L1001000111',	'MSpaapapa':'L1001001010',	'MSpaapapp':'L1001001011',	'MSpapaaaa':'L1001010000',	'MSpapaaap':'L1001010001',	'MSpapaapp':'L1001010011',	'MSpapapaa':'L1001010100',	'MSpapappa':'L1001010110',	'MSpapappp':'L1001010111',	'MSpapppaa':'L1001011100',	'MSpapppap':'L1001011101',	'MSpappppa':'L1001011110',	'MSpappppp':'L1001011111',	'MSppaaaad':'L1001100000',	'MSppaaaav':'L1001100001',	'MSppapaaa':'L1001101000',	'MSppapaap':'L1001101001',	'MSaaaaapap':'L10000000101',	'MSaapaapaa':'L10000100100',	'MSpapaapaa':'L10010100100',	'MSpaapp':'L10010011',	'MSaaappa':'L100000110',	'MSapaapa':'L100010010',	'MSapaapp':'L100010011',	'MSappaap':'L100011001',	'MSappapa':'L100011010',	'MSppaapa':'L100110010',	'MSpppaaa':'L100111000',	'MSpppaap':'L100111001',	'MSpppapa':'L100111010',	'MSaaaapaa':'L1000000100',	'MSaaaappa':'L1000000110',	'MSaapapap':'L1000010101',	'MSpaaaaaa':'L1001000000',	'MSpaaaaap':'L1001000001',	'MSpaaapaa':'L1001000100',	'MSpaaapap':'L1001000101',	'MSpaapaaa':'L1001001000',	'MSpaapaap':'L1001001001',	'MSpapapap':'L1001010101',	'MSaaaaapaa':'L10000000100',	'MSaapaapap':'L10000100101',	'MSpapaapap':'L10010100101',	'MSaaaaa':'L10000000',	'MSaaaap':'L10000001',	'MSaaapa':'L10000010',	'MSaaapp':'L10000011',	'MSaapaa':'L10000100',	'MSaapap':'L10000101',	'MSaappa':'L10000110',	'MSaappp':'L10000111',	'MSapaaa':'L10001000',	'MSapaap':'L10001001',	'MSapapa':'L10001010',	'MSapapp':'L10001011',	'MSappaa':'L10001100',	'MSappap':'L10001101',	'MSapppa':'L10001110',	'MSapppp':'L10001111',	'MSpaaaa':'L10010000',	'MSpaaap':'L10010001',	'MSpaapa':'L10010010',	'MSpapaa':'L10010100',	'MSpapap':'L10010101',	'MSpappa':'L10010110',	'MSpappp':'L10010111',	'MSppaaa':'L10011000',	'MSppaap':'L10011001',	'MSppapa':'L10011010',	'MSppapp':'L10011011',	'MSpppaa':'L10011100',	'MSpppap':'L10011101',	'MSppppa':'L10011110',	'MSppppp':'L10011111',	'MSaaaaaa':'L100000000',	'MSaaaaap':'L100000001',	'MSaaaapa':'L100000010',	'MSaaaapp':'L100000011',	'MSaaapaa':'L100000100',	'MSaaapap':'L100000101',	'MSaapaaa':'L100001000',	'MSaapaap':'L100001001',	'MSaapapa':'L100001010',	'MSaapapp':'L100001011',	'MSaapppa':'L100001110',	'MSaapppp':'L100001111',	'MSapaaaa':'L100010000',	'MSapapaa':'L100010100',	'MSpaaaaa':'L100100000',	'MSpaaaap':'L100100001',	'MSpaaapa':'L100100010',	'MSpaaapp':'L100100011',	'MSpaapaa':'L100100100',	'MSpaapap':'L100100101',	'MSpapaaa':'L100101000',	'MSpapaap':'L100101001',	'MSpapapa':'L100101010',	'MSpapapp':'L100101011',	'MSpapppa':'L100101110',	'MSpapppp':'L100101111',	'MSppaaaa':'L100110000',	'MSppapaa':'L100110100',	'MSaaaaapa':'L1000000010',	'MSaapaapa':'L1000010010',	'MSpapaapa':'L1001010010',	'MSaaaa':'L1000000',	'MSaaap':'L1000001',	'MSaapa':'L1000010',	'MSaapp':'L1000011',	'MSapaa':'L1000100',	'MSapap':'L1000101',	'MSappa':'L1000110',	'MSappp':'L1000111',	'MSpaaa':'L1001000',	'MSpaap':'L1001001',	'MSpapa':'L1001010',	'MSpapp':'L1001011',	'MSppaa':'L1001100',	'MSppap':'L1001101',	'MSpppa':'L1001110',	'MSpppp':'L1001111',	'MSaaa':'L100000',	'MSaap':'L100001',	'MSapa':'L100010',	'MSapp':'L100011',	'MSpaa':'L100100',	'MSpap':'L100101',	'MSppa':'L100110',	'MSppp':'L100111',	'MSaa':'L10000',	'MSap':'L10001',	'MSpa':'L10010',	'MSpp':'L10011',	'MSa':'L1000',	'MSp':'L1001',	'MS':'L100',	'Z2':'L11110',	'Z3':'L11111',	'P4':'L1111',	'P3':'L111',	'P2':'L11',	'P1':'L1',	'P0':'L',	'EMS':'L10'}
relpace_name_sheet = pd.DataFrame([dict_cell_name]).T
relpace_name_sheet.reset_index(inplace=True)
relpace_name_sheet.columns = ['cell_name', 'replace_name']

cell_name_to_relpace_name_sheet = relpace_name_sheet.set_index("cell_name")
relpace_name_to_cell_name_sheet = relpace_name_sheet.set_index("replace_name")

funder_cell = {'P0':'L', 'AB':'L0', 'P1':'L1', 'EMS':'L10', 'P2':'L11', 'MS':'L100', 'E':'L101', 'C':'L110', 'D':'L1110', 'P4':'L1111', 'Z2':'L11110', 'Z3':'L11111'}

transform = {'a':'0', 'p':'1', 'l':'0', 'r':'1', 'd':'0', 'v':'1'}


def except_cell(cell_name):
    
    transform_name = None
    
    if cell_name[0] == 'L':
        
        len_cell_name = len(cell_name)
        
        for i in range(1,len_cell_name+1):
            
            if cell_name[:-i] in list(relpace_name_to_cell_name_sheet.index.values):
                
                transform_name = (relpace_name_to_cell_name_sheet.loc[[cell_name[:-i]]].values[0])[0]
                break
            
        append_name = cell_name[len_cell_name-i:]
        
        for j in append_name:
            
            if j == '0':
                transform_name+='a'
            else:
                transform_name+='p'
                
    else:
        
        len_cell_name = len(cell_name)
        
        for i in range(1,len_cell_name+1):
            
            if cell_name[:-i] in list(cell_name_to_relpace_name_sheet.index.values):
                
                transform_name = (cell_name_to_relpace_name_sheet.loc[[cell_name[:-i]]].values[0])[0]
                break
            
        append_name = cell_name[len_cell_name-i:]
        
        for j in append_name:
            
            transform_name += transform[j]
    
    return transform_name
        
####
def cell_name_transfer(cell_list):
    
    transfer_cell_list = []
    if len(cell_list) == 0:
        pass
        
    elif type(cell_list) != list:
        if cell_list[0] == "L":
            
            if cell_list in list(relpace_name_to_cell_name_sheet.index.values):
            
                transfer_cell_list = (relpace_name_to_cell_name_sheet.loc[[cell_list]].values[0])[0]
                
            else:
                
                transfer_cell_list = except_cell(cell_list)
        else:
            if cell_list in list(cell_name_to_relpace_name_sheet.index.values):
                
                transfer_cell_list = (cell_name_to_relpace_name_sheet.loc[[cell_list]].values[0])[0]
            
            else:
                transfer_cell_list = except_cell(cell_list)

                
            
    else:
        if cell_list[0][0] == "L":
            for i in cell_list:
                
                if i in list(relpace_name_to_cell_name_sheet.index.values):
            
                    transfer_cell_list.append((relpace_name_to_cell_name_sheet.loc[[i]].values[0])[0])
                
                else:
                
                    transfer_cell_list.append(except_cell(i))

            
        else:
            for i in cell_list:
                
                if i in list(cell_name_to_relpace_name_sheet.index.values):
                    
                    transfer_cell_list.append((cell_name_to_relpace_name_sheet.loc[[i]].values[0])[0])
                    
                else:
                    
                    transfer_cell_list.append(except_cell(i))

    
    return transfer_cell_list
            

######
def lineage_order(cell_list):
    
    if cell_list[0][0] == "L":
        cell_list = cell_name_transfer(cell_list)
    else:
        pass
    
    cell_list_replace = cell_name_transfer(cell_list)
    cell_list_replace.sort()
    cell_list_replace = sorted(cell_list_replace, reverse=False, key=len)
    cell_list = cell_name_transfer(cell_list_replace)
    
    AB = []
    E = []
    MS = []
    D = []
    P = []
    C = []
    
    for i in cell_list:
        if i[0] == "A":
            AB.append(i)
        elif i[0] == "C":
            C.append(i)
        elif i[0] == "D":
            D.append(i)
        elif i[0] == "E":
            E.append(i)
        elif i[0] == "M":
            MS.append(i)  
        else:
            P.append(i)
    AB.sort()
    E.sort()
    MS.sort()
    D.sort()
    P.sort()
    C.sort()    
    lineage_cell_list = AB+MS+E+C+D+P  
    
    return lineage_cell_list
####
def get_terminal_cell(cell_list):
    
    if cell_list[0][0] == "L":
        cell_list = cell_name_transfer(cell_list)
    else:
        pass
    
    unique_cell_set = set(cell_list)
    unique_cell_list = list(unique_cell_set)
    transfer_cell_list = cell_name_transfer(unique_cell_list)
    transfer_cell_set = set(transfer_cell_list)
    
    not_terminal_list = []
    for i in transfer_cell_list:
        len_i = len(i)
        for j in transfer_cell_list:
            if len(j) <= len_i:
                pass
            else:
                if j[:len_i] == i:
                    not_terminal_list.append(i)
                    break
    
    
    terminal_cell_set = transfer_cell_set - set(not_terminal_list)

    terminal_cell_list = list(terminal_cell_set)
    terminal_cell_list = cell_name_transfer(terminal_cell_list)
    terminal_cell_list = lineage_order(terminal_cell_list)
    return terminal_cell_list

cell_list_AB16=['ABalaa','ABalap','ABalpa','ABalpp','ABaraa','ABarap','ABarpa','ABarpp','ABplaa','ABplap','ABplpa','ABplpp','ABpraa','ABprap','ABprpa','ABprpp','Ca','Cp','D','Ea','Ep','MSaa','MSap','MSpa','MSpp','P4']
cell_list_AB32=['ABalaaa','ABalaap','ABalapa','ABalapp','ABalpaa','ABalpap','ABalppa','ABalppp','ABaraaa','ABaraap','ABarapa','ABarapp','ABarpaa','ABarpap','ABarppa','ABarppp','ABplaaa','ABplaap','ABplapa','ABplapp','ABplpaa','ABplpap','ABplppa','ABplppp','ABpraaa','ABpraap','ABprapa','ABprapp','ABprpaa','ABprpap','ABprppa','ABprppp','Caa','Cap','Cpa','Cpp','Da','Dp','Eal','Ear','Epl','Epr','MSaaa','MSaap','MSapa','MSapp','MSpaa','MSpap','MSppa','MSppp','P4']
cell_list_AB64=['ABalaaaa','ABalaaap','ABalaapa','ABalaapp','ABalapaa','ABalapap','ABalappa','ABalappp','ABalpaaa','ABalpaap','ABalpapa','ABalpapp','ABalppaa','ABalppap','ABalpppa','ABalpppp','ABaraaaa','ABaraaap','ABaraapa','ABaraapp','ABarapaa','ABarapap','ABarappa','ABarappp','ABarpaaa','ABarpaap','ABarpapa','ABarpapp','ABarppaa','ABarppap','ABarpppa','ABarpppp','ABplaaaa','ABplaaap','ABplaapa','ABplaapp','ABplapaa','ABplapap','ABplappa','ABplappp','ABplpaaa','ABplpaap','ABplpapa','ABplpapp','ABplppaa','ABplppap','ABplpppa','ABplpppp','ABpraaaa','ABpraaap','ABpraapa','ABpraapp','ABprapaa','ABprapap','ABprappa','ABprappp','ABprpaaa','ABprpaap','ABprpapa','ABprpapp','ABprppaa','ABprppap','ABprpppa','ABprpppp','Caaa','Caap','Capa','Capp','Cpaa','Cpap','Cppa','Cppp','Da','Dp','Eal','Ear','Epl','Epr','MSaaaa','MSaaap','MSaapa','MSaapp','MSapaa','MSapap','MSappa','MSappp','MSpaaa','MSpaap','MSpapa','MSpapp','MSppaa','MSppap','MSpppa','MSpppp','Z2','Z3']
cell_list_AB128=['ABalaaaal','ABalaaaar','ABalaaapa','ABalaaapp','ABalaapaa','ABalaapap','ABalaappa','ABalaappp','ABalapaaa','ABalapaap','ABalapapa','ABalapapp','ABalappaa','ABalappap','ABalapppa','ABalapppp','ABalpaaaa','ABalpaaap','ABalpaapa','ABalpaapp','ABalpapaa','ABalpapap','ABalpappa','ABalpappp','ABalppaaa','ABalppaap','ABalppapa','ABalppapp','ABalpppaa','ABalpppap','ABalppppa','ABalppppp','ABaraaaaa','ABaraaaap','ABaraaapa','ABaraaapp','ABaraapaa','ABaraapap','ABaraappa','ABaraappp','ABarapaaa','ABarapaap','ABarapapa','ABarapapp','ABarappaa','ABarappap','ABarapppa','ABarapppp','ABarpaaaa','ABarpaaap','ABarpaapa','ABarpaapp','ABarpapaa','ABarpapap','ABarpappa','ABarpappp','ABarppaaa','ABarppaap','ABarppapa','ABarppapp','ABarpppaa','ABarpppap','ABarppppa','ABarppppp','ABplaaaaa','ABplaaaap','ABplaaapa','ABplaaapp','ABplaapaa','ABplaapap','ABplaappa','ABplaappp','ABplapaaa','ABplapaap','ABplapapa','ABplapapp','ABplappaa','ABplappap','ABplapppa','ABplapppp','ABplpaaaa','ABplpaaap','ABplpaapa','ABplpaapp','ABplpapaa','ABplpapap','ABplpappa','ABplpappp','ABplppaaa','ABplppaap','ABplppapa','ABplppapp','ABplpppaa','ABplpppap','ABplppppa','ABplppppp','ABpraaaaa','ABpraaaap','ABpraaapa','ABpraaapp','ABpraapaa','ABpraapap','ABpraappa','ABpraappp','ABprapaaa','ABprapaap','ABprapapa','ABprapapp','ABprappaa','ABprappap','ABprapppa','ABprapppp','ABprpaaaa','ABprpaaap','ABprpaapa','ABprpaapp','ABprpapaa','ABprpapap','ABprpappa','ABprpappp','ABprppaaa','ABprppaap','ABprppapa','ABprppapp','ABprpppaa','ABprpppap','ABprppppa','ABprppppp','MSaaaaa','MSaaaap','MSaaapa','MSaaapp','MSaapaa','MSaapap','MSaappa','MSaappp','MSapaaa','MSapaap','MSapapa','MSapapp','MSappaa','MSappap','MSapppa','MSapppp','MSpaaaa','MSpaaap','MSpaapa','MSpaapp','MSpapaa','MSpapap','MSpappa','MSpappp','MSppaaa','MSppaap','MSppapa','MSppapp','MSpppaa','MSpppap','MSppppa','MSppppp','Eala','Ealp','Eara','Earp','Epla','Eplp','Epra','Eprp','Caaaa','Caaap','Caapa','Caapp','Capaa','Capap','Cappa','Cappp','Cpaaa','Cpaap','Cpapa','Cpapp','Cppaa','Cppap','Cpppa','Cpppp','Daa','Dap','Dpa','Dpp','Z2','Z3']
cell_list_AB256=['ABalaaaala','ABalaaaalp','ABalaaaarl','ABalaaaarr','ABalaaapal','ABalaaapar','ABalaaappl','ABalaaappr','ABalaapaaa','ABalaapaap','ABalaapapa','ABalaapapp','ABalaappaa','ABalaappap','ABalaapppa','ABalaapppp','ABalapaaaa','ABalapaaap','ABalapaapa','ABalapaapp','ABalapapaa','ABalapapap','ABalapappa','ABalapappp','ABalappaaa','ABalappaap','ABalappapa','ABalappapp','ABalapppaa','ABalapppap','ABalappppa','ABalappppp','ABalpaaaaa','ABalpaaaap','ABalpaaapa','ABalpaaapp','ABalpaapaa','ABalpaapap','ABalpaappa','ABalpaappp','ABalpapaaa','ABalpapaap','ABalpapapa','ABalpapapp','ABalpappaa','ABalpappap','ABalpapppa','ABalpapppp','ABalppaaaa','ABalppaaap','ABalppaapa','ABalppaapp','ABalppapaa','ABalppapap','ABalppappa','ABalppappp','ABalpppaaa','ABalpppaap','ABalpppapa','ABalpppapp','ABalppppaa','ABalppppap','ABalpppppa','ABalpppppp','ABaraaaaaa','ABaraaaaap','ABaraaaapa','ABaraaaapp','ABaraaapaa','ABaraaapap','ABaraaappa','ABaraaappp','ABaraapaaa','ABaraapaap','ABaraapapa','ABaraapapp','ABaraappaa','ABaraappap','ABaraapppa','ABaraapppp','ABarapaaaa','ABarapaaap','ABarapaapa','ABarapaapp','ABarapapaa','ABarapapap','ABarapappa','ABarapappp','ABarappaaa','ABarappaap','ABarappapa','ABarappapp','ABarapppaa','ABarapppap','ABarappppa','ABarappppp','ABarpaaaaa','ABarpaaaap','ABarpaaapa','ABarpaaapp','ABarpaapaa','ABarpaapap','ABarpaappa','ABarpaappp','ABarpapaaa','ABarpapaap','ABarpapapa','ABarpapapp','ABarpappaa','ABarpappap','ABarpapppa','ABarpapppp','ABarppaaaa','ABarppaaap','ABarppaapa','ABarppaapp','ABarppapaa','ABarppapap','ABarppappa','ABarppappp','ABarpppaaa','ABarpppaap','ABarpppapa','ABarpppapp','ABarppppaa','ABarppppap','ABarpppppa','ABarpppppp','ABplaaaaaa','ABplaaaaap','ABplaaaapa','ABplaaaapp','ABplaaapaa','ABplaaapap','ABplaaappa','ABplaaappp','ABplaapaaa','ABplaapaap','ABplaapapa','ABplaapapp','ABplaappaa','ABplaappap','ABplaapppa','ABplaapppp','ABplapaaaa','ABplapaaap','ABplapaapa','ABplapaapp','ABplapapaa','ABplapapap','ABplapappa','ABplapappp','ABplappaaa','ABplappaap','ABplappapa','ABplappapp','ABplapppaa','ABplapppap','ABplappppa','ABplappppp','ABplpaaaaa','ABplpaaaap','ABplpaaapa','ABplpaaapp','ABplpaapaa','ABplpaapap','ABplpaappa','ABplpaappp','ABplpapaaa','ABplpapaap','ABplpapapa','ABplpapapp','ABplpappaa','ABplpappap','ABplpapppa','ABplpapppp','ABplppaaaa','ABplppaaap','ABplppaapa','ABplppaapp','ABplppapaa','ABplppapap','ABplppappa','ABplppappp','ABplpppaaa','ABplpppaap','ABplpppapa','ABplpppapp','ABplppppaa','ABplppppap','ABplpppppa','ABplpppppp','ABpraaaaaa','ABpraaaaap','ABpraaaapa','ABpraaaapp','ABpraaapaa','ABpraaapap','ABpraaappa','ABpraaappp','ABpraapaaa','ABpraapaap','ABpraapapa','ABpraapapp','ABpraappaa','ABpraappap','ABpraapppa','ABpraapppp','ABprapaaaa','ABprapaaap','ABprapaapa','ABprapaapp','ABprapapaa','ABprapapap','ABprapappa','ABprapappp','ABprappaaa','ABprappaap','ABprappapa','ABprappapp','ABprapppaa','ABprapppap','ABprappppa','ABprappppp','ABprpaaaaa','ABprpaaaap','ABprpaaapa','ABprpaaapp','ABprpaapaa','ABprpaapap','ABprpaappa','ABprpaappp','ABprpapaaa','ABprpapaap','ABprpapapa','ABprpapapp','ABprpappaa','ABprpappap','ABprpapppa','ABprpapppp','ABprppaaaa','ABprppaaap','ABprppaapa','ABprppaapp','ABprppapaa','ABprppapap','ABprppappa','ABprppappp','ABprpppaaa','ABprpppaap','ABprpppapa','ABprpppapp','ABprppppaa','ABprppppap','ABprpppppa','ABprpppppp','Caaaaa','Caaaap','Caaapa','Caaapp','Caapa','Caappd','Caappv','Capaaa','Capaap','Capapa','Capapp','Cappaa','Cappap','Capppa','Capppp','Cpaaaa','Cpaaap','Cpaapa','Cpaapp','Cpapaa','Cpapap','Cpappd','Cpappv','Cppaaa','Cppaap','Cppapa','Cppapp','Cpppaa','Cpppap','Cppppa','Cppppp','Daaa','Daap','Dapa','Dapp','Dpaa','Dpap','Dppa','Dppp','Ealaa','Ealap','Ealpa','Ealpp','Earaa','Earap','Earpa','Earpp','Eplaa','Eplap','Eplpa','Eplpp','Epraa','Eprap','Eprpa','Eprpp','MSaaaaaa','MSaaaaap','MSaaaapa','MSaaaapp','MSaaapaa','MSaaapap','MSaaapp','MSaapaaa','MSaapaap','MSaapapa','MSaapapp','MSaappa','MSaappp','MSapaaaa','MSapaaap','MSapaap','MSapapaa','MSapapap','MSapappa','MSapappp','MSappaa','MSappap','MSapppa','MSapppp','MSpaaaaa','MSpaaaap','MSpaaapa','MSpaaapp','MSpaapaa','MSpaapap','MSpaapp','MSpapaaa','MSpapaap','MSpapapa','MSpapapp','MSpappa','MSpappp','MSppaaaa','MSppaaap','MSppaap','MSppapaa','MSppapap','MSppappa','MSppappp','MSpppaa','MSpppap','MSppppa','MSppppp','Z2','Z3']


def stage_cell_list(children_cell):
    cell=children_cell
    if cell in cell_list_AB16:
        stage_cell_list=cell_list_AB16   
    elif cell in cell_list_AB32:
        stage_cell_list=cell_list_AB32
    elif cell in cell_list_AB64:
        stage_cell_list=cell_list_AB64 
    elif cell in cell_list_AB128:
        stage_cell_list=cell_list_AB128 
    elif cell in cell_list_AB256:
        stage_cell_list=cell_list_AB256    
    return stage_cell_list     

##############################################################################

cell_list=['ABal', 'ABala', 'ABalaa', 'ABalaaa', 'ABalaaaa', 'ABalaaaal', 'ABalaaaala', 'ABalaaaalp', 'ABalaaaar', 'ABalaaaarl', 'ABalaaaarr', 'ABalaaap', 'ABalaaapa', 'ABalaaapal', 'ABalaaapar', 'ABalaaapp', 'ABalaaappl', 'ABalaaappr', 'ABalaap', 'ABalaapa', 'ABalaapaa', 'ABalaapaaa', 'ABalaapaap', 'ABalaapap', 'ABalaapapa', 'ABalaapapp', 'ABalaapp', 'ABalaappa', 'ABalaappaa', 'ABalaappap', 'ABalaappp', 'ABalaapppa', 'ABalaapppp', 'ABalap', 'ABalapa', 'ABalapaa', 'ABalapaaa', 'ABalapaaaa', 'ABalapaaap', 'ABalapaap', 'ABalapaapa', 'ABalapaapp', 'ABalapap', 'ABalapapa', 'ABalapapaa', 'ABalapapap', 'ABalapapp', 'ABalapappa', 'ABalapappp', 'ABalapp', 'ABalappa', 'ABalappaa', 'ABalappaaa', 'ABalappaap', 'ABalappap', 'ABalappapa', 'ABalappapp', 'ABalappp', 'ABalapppa', 'ABalapppaa', 'ABalapppap', 'ABalapppp', 'ABalappppa', 'ABalappppp', 'ABalp', 'ABalpa', 'ABalpaa', 'ABalpaaa', 'ABalpaaaa', 'ABalpaaaaa', 'ABalpaaaap', 'ABalpaaap', 'ABalpaaapa', 'ABalpaaapp', 'ABalpaap', 'ABalpaapa', 'ABalpaapaa', 'ABalpaapap', 'ABalpaapp', 'ABalpaappa', 'ABalpaappp', 'ABalpap', 'ABalpapa', 'ABalpapaa', 'ABalpapaaa', 'ABalpapaap', 'ABalpapap', 'ABalpapapa', 'ABalpapapp', 'ABalpapp', 'ABalpappa', 'ABalpappaa', 'ABalpappap', 'ABalpappp', 'ABalpapppa', 'ABalpapppp', 'ABalpp', 'ABalppa', 'ABalppaa', 'ABalppaaa', 'ABalppaaaa', 'ABalppaaap', 'ABalppaap', 'ABalppaapa', 'ABalppaapp', 'ABalppap', 'ABalppapa', 'ABalppapaa', 'ABalppapap', 'ABalppapp', 'ABalppappa', 'ABalppappp', 'ABalppp', 'ABalpppa', 'ABalpppaa', 'ABalpppaaa', 'ABalpppaap', 'ABalpppap', 'ABalpppapa', 'ABalpppapp', 'ABalpppp', 'ABalppppa', 'ABalppppaa', 'ABalppppap', 'ABalppppp', 'ABalpppppa', 'ABalpppppp', 'ABar', 'ABara', 'ABaraa', 'ABaraaa', 'ABaraaaa', 'ABaraaaaa', 'ABaraaaaaa', 'ABaraaaaap', 'ABaraaaap', 'ABaraaaapa', 'ABaraaaapp', 'ABaraaap', 'ABaraaapa', 'ABaraaapaa', 'ABaraaapap', 'ABaraaapp', 'ABaraaappa', 'ABaraaappp', 'ABaraap', 'ABaraapa', 'ABaraapaa', 'ABaraapaaa', 'ABaraapaap', 'ABaraapap', 'ABaraapapa', 'ABaraapapp', 'ABaraapp', 'ABaraappa', 'ABaraappaa', 'ABaraappap', 'ABaraappp', 'ABaraapppa', 'ABaraapppp', 'ABarap', 'ABarapa', 'ABarapaa', 'ABarapaaa', 'ABarapaaaa', 'ABarapaaap', 'ABarapaap', 'ABarapaapa', 'ABarapaapp', 'ABarapap', 'ABarapapa', 'ABarapapaa', 'ABarapapap', 'ABarapapp', 'ABarapappa', 'ABarapappp', 'ABarapp', 'ABarappa', 'ABarappaa', 'ABarappaaa', 'ABarappaap', 'ABarappap', 'ABarappapa', 'ABarappapp', 'ABarappp', 'ABarapppa', 'ABarapppaa', 'ABarapppap', 'ABarapppp', 'ABarappppa', 'ABarappppp', 'ABarp', 'ABarpa', 'ABarpaa', 'ABarpaaa', 'ABarpaaaa', 'ABarpaaaaa', 'ABarpaaaap', 'ABarpaaap', 'ABarpaaapa', 'ABarpaaapp', 'ABarpaap', 'ABarpaapa', 'ABarpaapaa', 'ABarpaapap', 'ABarpaapp', 'ABarpaappa', 'ABarpaappp', 'ABarpap', 'ABarpapa', 'ABarpapaa', 'ABarpapaaa', 'ABarpapaap', 'ABarpapap', 'ABarpapapa', 'ABarpapapp', 'ABarpapp', 'ABarpappa', 'ABarpappaa', 'ABarpappap', 'ABarpappp', 'ABarpapppa', 'ABarpapppp', 'ABarpp', 'ABarppa', 'ABarppaa', 'ABarppaaa', 'ABarppaaaa', 'ABarppaaap', 'ABarppaap', 'ABarppaapa', 'ABarppaapp', 'ABarppap', 'ABarppapa', 'ABarppapaa', 'ABarppapap', 'ABarppapp', 'ABarppappa', 'ABarppappp', 'ABarppp', 'ABarpppa', 'ABarpppaa', 'ABarpppaaa', 'ABarpppaap', 'ABarpppap', 'ABarpppapa', 'ABarpppapp', 'ABarpppp', 'ABarppppa', 'ABarppppaa', 'ABarppppap', 'ABarppppp', 'ABarpppppa', 'ABarpppppp', 'ABpl', 'ABpla', 'ABplaa', 'ABplaaa', 'ABplaaaa', 'ABplaaaaa', 'ABplaaaaaa', 'ABplaaaaap', 'ABplaaaap', 'ABplaaaapa', 'ABplaaaapp', 'ABplaaap', 'ABplaaapa', 'ABplaaapaa', 'ABplaaapap', 'ABplaaapp', 'ABplaaappa', 'ABplaaappp', 'ABplaap', 'ABplaapa', 'ABplaapaa', 'ABplaapaaa', 'ABplaapaap', 'ABplaapap', 'ABplaapapa', 'ABplaapapp', 'ABplaapp', 'ABplaappa', 'ABplaappaa', 'ABplaappap', 'ABplaappp', 'ABplaapppa', 'ABplaapppp', 'ABplap', 'ABplapa', 'ABplapaa', 'ABplapaaa', 'ABplapaaaa', 'ABplapaaap', 'ABplapaap', 'ABplapaapa', 'ABplapaapp', 'ABplapap', 'ABplapapa', 'ABplapapaa', 'ABplapapap', 'ABplapapp', 'ABplapappa', 'ABplapappp', 'ABplapp', 'ABplappa', 'ABplappaa', 'ABplappaaa', 'ABplappaap', 'ABplappap', 'ABplappapa', 'ABplappapp', 'ABplappp', 'ABplapppa', 'ABplapppaa', 'ABplapppap', 'ABplapppp', 'ABplappppa', 'ABplappppp', 'ABplp', 'ABplpa', 'ABplpaa', 'ABplpaaa', 'ABplpaaaa', 'ABplpaaaaa', 'ABplpaaaap', 'ABplpaaap', 'ABplpaaapa', 'ABplpaaapp', 'ABplpaap', 'ABplpaapa', 'ABplpaapaa', 'ABplpaapap', 'ABplpaapp', 'ABplpaappa', 'ABplpaappp', 'ABplpap', 'ABplpapa', 'ABplpapaa', 'ABplpapaaa', 'ABplpapaap', 'ABplpapap', 'ABplpapapa', 'ABplpapapp', 'ABplpapp', 'ABplpappa', 'ABplpappaa', 'ABplpappap', 'ABplpappp', 'ABplpapppa', 'ABplpapppp', 'ABplpp', 'ABplppa', 'ABplppaa', 'ABplppaaa', 'ABplppaaaa', 'ABplppaaap', 'ABplppaap', 'ABplppaapa', 'ABplppaapp', 'ABplppap', 'ABplppapa', 'ABplppapaa', 'ABplppapap', 'ABplppapp', 'ABplppappa', 'ABplppappp', 'ABplppp', 'ABplpppa', 'ABplpppaa', 'ABplpppaaa', 'ABplpppaap', 'ABplpppap', 'ABplpppapa', 'ABplpppapp', 'ABplpppp', 'ABplppppa', 'ABplppppaa', 'ABplppppap', 'ABplppppp', 'ABplpppppa', 'ABplpppppp', 'ABpr', 'ABpra', 'ABpraa', 'ABpraaa', 'ABpraaaa', 'ABpraaaaa', 'ABpraaaaaa', 'ABpraaaaap', 'ABpraaaap', 'ABpraaaapa', 'ABpraaaapp', 'ABpraaap', 'ABpraaapa', 'ABpraaapaa', 'ABpraaapap', 'ABpraaapp', 'ABpraaappa', 'ABpraaappp', 'ABpraap', 'ABpraapa', 'ABpraapaa', 'ABpraapaaa', 'ABpraapaap', 'ABpraapap', 'ABpraapapa', 'ABpraapapp', 'ABpraapp', 'ABpraappa', 'ABpraappaa', 'ABpraappap', 'ABpraappp', 'ABpraapppa', 'ABpraapppp', 'ABprap', 'ABprapa', 'ABprapaa', 'ABprapaaa', 'ABprapaaaa', 'ABprapaaap', 'ABprapaap', 'ABprapaapa', 'ABprapaapp', 'ABprapap', 'ABprapapa', 'ABprapapaa', 'ABprapapap', 'ABprapapp', 'ABprapappa', 'ABprapappp', 'ABprapp', 'ABprappa', 'ABprappaa', 'ABprappaaa', 'ABprappaap', 'ABprappap', 'ABprappapa', 'ABprappapp', 'ABprappp', 'ABprapppa', 'ABprapppaa', 'ABprapppap', 'ABprapppp', 'ABprappppa', 'ABprappppp', 'ABprp', 'ABprpa', 'ABprpaa', 'ABprpaaa', 'ABprpaaaa', 'ABprpaaaaa', 'ABprpaaaap', 'ABprpaaap', 'ABprpaaapa', 'ABprpaaapp', 'ABprpaap', 'ABprpaapa', 'ABprpaapaa', 'ABprpaapap', 'ABprpaapp', 'ABprpaappa', 'ABprpaappp', 'ABprpap', 'ABprpapa', 'ABprpapaa', 'ABprpapaaa', 'ABprpapaap', 'ABprpapap', 'ABprpapapa', 'ABprpapapp', 'ABprpapp', 'ABprpappa', 'ABprpappaa', 'ABprpappap', 'ABprpappp', 'ABprpapppa', 'ABprpapppp', 'ABprpp', 'ABprppa', 'ABprppaa', 'ABprppaaa', 'ABprppaaaa', 'ABprppaaap', 'ABprppaap', 'ABprppaapa', 'ABprppaapp', 'ABprppap', 'ABprppapa', 'ABprppapaa', 'ABprppapap', 'ABprppapp', 'ABprppappa', 'ABprppappp', 'ABprppp', 'ABprpppa', 'ABprpppaa', 'ABprpppaaa', 'ABprpppaap', 'ABprpppap', 'ABprpppapa', 'ABprpppapp', 'ABprpppp', 'ABprppppa', 'ABprppppaa', 'ABprppppap', 'ABprppppp', 'ABprpppppa', 'ABprpppppp', 'C', 'Ca', 'Caa', 'Caaa', 'Caaaa', 'Caaaaa', 'Caaaap', 'Caaap', 'Caaapa', 'Caaapp', 'Caap', 'Caapa', 'Caapp', 'Caappd', 'Caappv', 'Cap', 'Capa', 'Capaa', 'Capaaa', 'Capaap', 'Capap', 'Capapa', 'Capapp', 'Capp', 'Cappa', 'Cappaa', 'Cappap', 'Cappp', 'Capppa', 'Capppp', 'Cp', 'Cpa', 'Cpaa', 'Cpaaa', 'Cpaaaa', 'Cpaaap', 'Cpaap', 'Cpaapa', 'Cpaapp', 'Cpap', 'Cpapa', 'Cpapaa', 'Cpapap', 'Cpapp', 'Cpappd', 'Cpappv', 'Cpp', 'Cppa', 'Cppaa', 'Cppaaa', 'Cppaap', 'Cppap', 'Cppapa', 'Cppapp', 'Cppp', 'Cpppa', 'Cpppaa', 'Cpppap', 'Cpppp', 'Cppppa', 'Cppppp', 'D', 'Da', 'Daa', 'Daaa', 'Daap', 'Dap', 'Dapa', 'Dapp', 'Dp', 'Dpa', 'Dpaa', 'Dpap', 'Dpp', 'Dppa', 'Dppp', 'E', 'Ea', 'Eal', 'Eala', 'Ealaa', 'Ealap', 'Ealp', 'Ealpa', 'Ealpp', 'Ear', 'Eara', 'Earaa', 'Earap', 'Earp', 'Earpa', 'Earpp', 'Ep', 'Epl', 'Epla', 'Eplaa', 'Eplap', 'Eplp', 'Eplpa', 'Eplpp', 'Epr', 'Epra', 'Epraa', 'Eprap', 'Eprp', 'Eprpa', 'Eprpp', 'MS', 'MSa', 'MSaa', 'MSaaa', 'MSaaaa', 'MSaaaaa', 'MSaaaaaa', 'MSaaaaap', 'MSaaaap', 'MSaaaapa', 'MSaaaapp', 'MSaaap', 'MSaaapa', 'MSaaapaa', 'MSaaapap', 'MSaaapp', 'MSaap', 'MSaapa', 'MSaapaa', 'MSaapaaa', 'MSaapaap', 'MSaapap', 'MSaapapa', 'MSaapapp', 'MSaapp', 'MSaappa', 'MSaappp', 'MSap', 'MSapa', 'MSapaa', 'MSapaaa', 'MSapaaaa', 'MSapaaap', 'MSapaap', 'MSapap', 'MSapapa', 'MSapapaa', 'MSapapap', 'MSapapp', 'MSapappa', 'MSapappp', 'MSapp', 'MSappa', 'MSappaa', 'MSappap', 'MSappp', 'MSapppa', 'MSapppp', 'MSp', 'MSpa', 'MSpaa', 'MSpaaa', 'MSpaaaa', 'MSpaaaaa', 'MSpaaaap', 'MSpaaap', 'MSpaaapa', 'MSpaaapp', 'MSpaap', 'MSpaapa', 'MSpaapaa', 'MSpaapap', 'MSpaapp', 'MSpap', 'MSpapa', 'MSpapaa', 'MSpapaaa', 'MSpapaap', 'MSpapap', 'MSpapapa', 'MSpapapp', 'MSpapp', 'MSpappa', 'MSpappp', 'MSpp', 'MSppa', 'MSppaa', 'MSppaaa', 'MSppaaaa', 'MSppaaap', 'MSppaap', 'MSppap', 'MSppapa', 'MSppapaa', 'MSppapap', 'MSppapp', 'MSppappa', 'MSppappp', 'MSppp', 'MSpppa', 'MSpppaa', 'MSpppap', 'MSpppp', 'MSppppa', 'MSppppp', 'P3', 'P4', 'Z2', 'Z3']

File_list=[]
embryo_list=[]
Embryo_cell_dist=[]
Embryo_cell_std=[]
Embryo_dist_sum = np.zeros(shape=(len(cell_list),len(cell_list)))
Total_matrix=[]
n=0
os.chdir(Control_distance_matrix)

for file in os.listdir(Control_distance_matrix):
    n+=1
    Embryo=str.split(file,"_dist")[0]
    File_list.append(Embryo)
    Embryo_dist=pd.read_csv(file,index_col=0,header=0,sep='\t')
    Embryo_dist=Embryo_dist[cell_list].loc[cell_list]
    Embryo_dist_sum += Embryo_dist.values
    
    if type(Total_matrix) == list:
        Total_matrix = Embryo_dist                                 
    else:
        Total_matrix = pd.concat([Total_matrix, Embryo_dist], axis=0)
        
Embryo_dist_mean=Embryo_dist_sum/n
Embryo_dist_mean=pd.DataFrame(Embryo_dist_mean)
Embryo_dist_mean.index=cell_list
Embryo_dist_mean.columns=cell_list
##############################
RNAi_cell_position=RNAi_relative_cell_position_Qvalue_binary_001

replace_1=RNAi_cell_position.replace(-1,1)
replace_1=replace_1.sum(axis=0)
cell_position_phenotype_embryo=list(replace_1[replace_1!=0].index)
data=RNAi_cell_position[cell_position_phenotype_embryo]
RNAi_cell_position_1=data
  
total_cell_list=list(RNAi_cell_position.index)
total_cell_list=cell_name_transfer(total_cell_list)
RNAi_cell_position_1.index=total_cell_list

cell_pair=list(combinations(total_cell_list,2))
pair=[]
for i in cell_pair:
    cell1=i[0]
    cell2=i[1]
    if len(cell1)==len(cell2)-1 and cell1 in cell2:
        pair.append(i)

embryo_name_revise=[]
embryo_name_norevise=[]
mother_cell_revise=[]
mother_cell_norevise=[]
children_cell_revise=[]
children_cell_norevise=[]
revise_cell_pair=pd.DataFrame()
for i in RNAi_cell_position_1:
    embryo=RNAi_cell_position_1[i]
    
    for cell1,cell2 in pair: 
        if  embryo.loc[cell1]==1 and  embryo.loc[cell2]==0  and  embryo.loc[cell1] != np.nan and  embryo.loc[cell2] != np.nan:
            embryo_name_revise.append(i)
            mother_cell_revise.append(cell1)
            children_cell_revise.append(cell2)
        elif  embryo.loc[cell1]==1 and embryo.loc[cell2]==1 and  embryo.loc[cell1] != np.nan and  embryo.loc[cell2] != np.nan: 
            embryo_name_norevise.append(i)
            mother_cell_norevise.append(cell1)
            children_cell_norevise.append(cell2)
mother_cell_revise=cell_name_transfer(mother_cell_revise)
mother_cell_norevise=cell_name_transfer(mother_cell_norevise)

children_cell_revise=cell_name_transfer(children_cell_revise)  
children_cell_norevise=cell_name_transfer(children_cell_norevise)  

revise=pd.DataFrame(mother_cell_revise,columns=['mother cell'])
revise['children cell']=children_cell_revise
norevise=pd.DataFrame(mother_cell_norevise,columns=['mother cell'])
norevise['children cell']=children_cell_norevise

revise.index=embryo_name_revise
norevise.index=embryo_name_norevise

revise.to_csv(os.path.join(Output_Folder,"RNAi_position_correction.txt"), sep="\t")   
norevise.to_csv(os.path.join(Output_Folder,"RNAi_position_not_correction.txt"), sep="\t")  

#######################################################################################################
RNAi_cellposition_phenotype_zscore=RNAi_relative_cell_position_Zscore
RNAi_position_single_cell_RMSD_all=RNAi_relative_cell_position_RMSD
CTR_cell_position_RMSD=CTR_relative_cell_position_RMSD_mean
position_correction = revise
position_correction['correction']=1
position_not_correct = norevise
position_not_correct['correction']=0
position_info=pd.concat([position_correction,position_not_correct],axis=0)

######Keep the cell migration distance unchanged, random migration direction 
all_simulate_direction_RMSD=[]
all_simulate_zscore=[]
all_actual_zscore=[]
all_actual_RMSD=[]
mother_qvalues=[]
daughter_qvalues=[]
I=sympy.I
number=0
for i in range(len(position_info.index)):
    number+=1
    print(number)

    temp=position_info.iloc[i]
    embryo=temp.name
    children_cell=temp['children cell']
    cell_list_temp=stage_cell_list(children_cell)
       
    fil_name=embryo+'_XYZ.txt'
    embryo_xyz=pd.read_csv(os.path.join(RNAi_XYZ_folder,fil_name), index_col=0, sep='\t')
    embryo_xyz=embryo_xyz.T

    mother_cell_name=temp['mother cell']
    children_cell_name=temp['children cell']
    mother_xyz=np.array(embryo_xyz[mother_cell_name])
    children_xyz=np.array(embryo_xyz[children_cell_name])            
    x,y,z=sympy.symbols('x,y,z')
    a,b,c= mother_xyz[0], mother_xyz[1], mother_xyz[2]

    distance=(np.sum(np.square(children_xyz - mother_xyz)))**0.5
    new_XYZ=[99.0 + 0.6*I,99.0 + 0.6*I,99.0 + 0.6*I]        
    while type(new_XYZ[0])==sympy.add.Add or type(new_XYZ[1])==sympy.add.Add or type(new_XYZ[2])==sympy.add.Add:        
        x_random=random.uniform(0, distance)            
        x_simulate=[a+x_random,a-x_random]
        
        range_y=(distance**2-(x_random)**2)**0.5            
        y_random=random.uniform(0, range_y)
        y_simulate=[a+y_random,a-y_random]
        
        z_simulate=sympy.solve(x_random**2+y_random**2 +(z-c)**2-distance**2,z)
        
        X=random.sample(x_simulate, 1)[0]
        Y=random.sample(y_simulate, 1)[0]
        Z=random.sample(z_simulate, 1)[0]
        new_XYZ=[X,Y,Z]
    embryo_xyz[children_cell_name]=new_XYZ

    embryo_xyz=embryo_xyz.T
  
    cell_pair_distance=scipy.spatial.distance.pdist(embryo_xyz)
    dist_max=RNAi_embryo_length.loc[embryo]['embryo length']
    cell_pair_distance=cell_pair_distance/dist_max
    cell_pair_distance=pd.DataFrame(scipy.spatial.distance.squareform(cell_pair_distance),
                                    index=embryo_xyz.index,columns=embryo_xyz.index)
    
    cell_vactor_temp=cell_pair_distance[children_cell_name]
    cell_vactor_mean=Embryo_dist_mean[children_cell_name]
    cell_vactor=pd.concat([pd.DataFrame(cell_vactor_temp),pd.DataFrame(cell_vactor_mean)],axis=1)
    cell_vactor=cell_vactor.drop([children_cell_name]).dropna()
    if len(cell_vactor)>0:
        cell_vactor=cell_vactor.T
        cell_rmsd=scipy.spatial.distance.pdist(cell_vactor)/len(cell_vactor.columns)**0.5
    else:
        cell_rmsd=np.array([np.nan])
    all_simulate_direction_RMSD.append(cell_rmsd[0])
    control_mean=CTR_cell_position_RMSD.loc[children_cell_name]['cell_rmsd_mean']   
    control_std=CTR_cell_position_RMSD.loc[children_cell_name]['cell_rmsd_sd']   
    simulate_zscore=(cell_rmsd[0]-control_mean)/control_std    
    all_simulate_zscore.append(simulate_zscore)    
    actual_zscore=RNAi_cellposition_phenotype_zscore.loc[children_cell_name][embryo]        
    all_actual_zscore.append(actual_zscore)    
    actrual_RMSD=RNAi_position_single_cell_RMSD_all.loc[children_cell_name][embryo] 
    all_actual_RMSD.append(actrual_RMSD)    
    mother_qvalue=RNAi_relative_cell_position_Qvalue.loc[mother_cell_name][embryo] 
    mother_qvalues.append(mother_qvalue)    
    daughter_qvalue=RNAi_relative_cell_position_Qvalue.loc[children_cell_name][embryo] 
    daughter_qvalues.append(daughter_qvalue)    
position_info['actrual RMSD']=  all_actual_RMSD     
position_info['simulate RMSD']=  all_simulate_direction_RMSD      
position_info['actrual zscore']=  all_actual_zscore      
position_info['simulate zscore']=  all_simulate_zscore      
position_info['mother_qvalues']=  mother_qvalues      
position_info['daughter_qvalues']=  daughter_qvalues      
       
#position_info.to_csv(r'C:\Users\dell\Desktop\position_direction_simulation.txt', sep="\t")

#######################################################################################
position_direction_simulation=position_info

reference_cell_number_all=[]
abnormal_cell_number_all=[]
abnormal_rate_all=[]
reference_cell_number_all_mother=[]
abnormal_cell_number_all_mother=[]
abnormal_rate_all_mother=[]
a=0
for i in range(len(position_direction_simulation.index)):
    a+=1
    print(a)

    temp=position_direction_simulation.iloc[i]
    embryo=temp.name
    children_cell=temp['children cell']
    mother_cell=temp['mother cell']

    detected_cell_list=stage_cell_list(children_cell)
    detected_cell_list_mother=stage_cell_list(mother_cell)

    cell_position_phenotype_temp=RNAi_cell_position.loc[detected_cell_list][embryo].dropna()
    cell_position_phenotype_temp_mother=RNAi_cell_position.loc[detected_cell_list_mother][embryo].dropna()

    reference_cell_number=cell_position_phenotype_temp.count()
    reference_cell_number_mother=cell_position_phenotype_temp_mother.count()
    
    abnormal_cell_number=cell_position_phenotype_temp[cell_position_phenotype_temp==1].count()
    abnormal_cell_number_mother=cell_position_phenotype_temp_mother[cell_position_phenotype_temp_mother==1].count()

    
    abnormal_rate=abnormal_cell_number/reference_cell_number
    abnormal_rate_mother=abnormal_cell_number_mother/reference_cell_number_mother
    
    reference_cell_number_all.append(reference_cell_number)
    abnormal_cell_number_all.append(abnormal_cell_number)
    abnormal_rate_all.append(abnormal_rate)
    
    reference_cell_number_all_mother.append(reference_cell_number_mother)
    abnormal_cell_number_all_mother.append(abnormal_cell_number_mother)
    abnormal_rate_all_mother.append(abnormal_rate_mother)
    
#position_direction_simulation['reference_cell_number_children'] =   reference_cell_number_all
#position_direction_simulation['abnormal_cell_number_children']  =  abnormal_cell_number_all
position_direction_simulation['abnormal_rate'] = abnormal_rate_all
#position_direction_simulation['reference_cell_number_mother'] =   reference_cell_number_all_mother
#position_direction_simulation['abnormal_cell_number_mother']  =  abnormal_cell_number_all_mother
#position_direction_simulation['abnormal_rate_mother'] = abnormal_rate_all_mother

position_direction_simulation.to_csv(os.path.join(Output_Folder,output_real_and_simulation_position_correction+'.txt'), sep="\t")





































