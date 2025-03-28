# coding utf-8
"""
Code for obtaining input for non stationary temporal MIIC.
Author: Tiziana Tocci
"""

"""
### Set working directory
"""
import os
script_dir = r"spheroid_morpho_ML/MIIC" # adjust your own path
os.chdir(script_dir)


"""
### Libraries
"""
import pandas as pd
from modules.functions_step1 import lag_final_data, save_all_inputs

"""
### Directories
"""
data_dir = r"../machine_learning_classification/data"
result_dir = r"./results"

"""
### Load files and lag them in the appropriate way for MIIC analysus
"""
A673_features_final = pd.read_csv(os.path.join(data_dir, "processed_data", "A673_processed_data.csv"))
PDX_features_final = pd.read_csv(os.path.join(data_dir, "processed_data", "PDX_processed_data.csv"))

A673_features_final = A673_features_final.rename(columns={'spheroid ID': 'UniqueIdentifier'})
PDX_features_final = PDX_features_final.rename(columns={'spheroid ID': 'UniqueIdentifier'})

# lag variables
variables_to_lag = ['Area (um2)',
                    'Perimeter (um)',
                    'Solidity',
                    'Equivalent Diameter (um)',
                    'Circularity',
                    'Mean grey value',
                    'Homogeneity',
                    'Energy',
                    'Correlation']
other_vars = ['Experiment ID', 'drug concentration (uM)', 'spheroIndex',
              'Growth1-0', 'Growth2-0', 'Growth2-1', 'Grey1-0', 'Grey2-0', 'Grey2-1',
              'viability score', '2 classes encoded', 
              '3 classes encoded', 'UniqueIdentifier', 'Origin']
final_columns=['Experiment ID', 'ts', 'drug concentration (uM)', 'spheroIndex',
 'Area (um2)', 'Perimeter (um)', 'Solidity', 'Equivalent Diameter (um)',
 'Circularity', 'Mean grey value', 'Homogeneity', 'Energy', 'Correlation',
 'viability score', 'UniqueIdentifier', '2 classes encoded', '3 classes encoded',
 'Origin', 'Growth1-0', 'Growth2-1', 'Growth2-0', 'Grey1-0', 'Grey2-1', 'Grey2-0']

_, df = lag_final_data(A673_features_final, PDX_features_final, variables_to_lag, other_vars, final_columns)

# save all MIIC inputs 
save_all_inputs(df, result_dir)
