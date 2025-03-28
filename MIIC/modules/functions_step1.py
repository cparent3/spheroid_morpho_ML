# -*- coding: utf-8 -*-
"""
Functions for step 1
Author: Tiziana Tocci
"""

import os
import pandas as pd
import numpy as np


def select_one_condition(df, cond_column, cond_to_select):
    """
    Function to select part of dataframe based on a condition.

    Parameters
    ----------
    df : pandas dataframe
    cond_column : string
    cond_to_select : string

    Returns
    -------
    df_cond : pandas dataframe
    """
    
    unique_id_cond = df[df[cond_column] == cond_to_select]["UniqueIdentifier"]
    df_cond = df[df["UniqueIdentifier"].isin(unique_id_cond)]
    df_cond=df_cond.drop(columns=cond_column)

    return df_cond


def save_df_origin(df, which_class, result_dir, which_via):
    """
    Save separate dataframes based on wheter the spheroid's origin is cell line or pdx.

    Parameters
    ----------
    df : pandas dataframe
    which_class : string
    result_dir : string
    which_via : string. Whether to save the file with or without the viability column


    Returns
    -------
    df_line : pandas dataframe
    df_pdx : pandas dataframe

    """
    # create line and pdx subdataframes
    df_line=select_one_condition(df, "Origin", "line")
    df_pdx=select_one_condition(df, "Origin", "pdx")
    # save both subdataframes
    df_line.to_csv(
        os.path.join(result_dir, f"inputmiictns_{which_class}_{which_via}_line.csv"), index=False) 
    df_pdx.to_csv(
        os.path.join(result_dir, f"inputmiictns_{which_class}_{which_via}_pdx.csv"), index=False) 
    
    return df_line, df_pdx 


def save_inputs(real_input, list_column_to_drop,\
                which_class, result_dir):
    """
    Save files for MIIC.

    Parameters
    ----------
    real_input : pandas dataframe
    list_column_to_drop : list of strings
    which_class : string
    result_dir : string


    Returns
    -------
    oneclass_input_woviability : pandas dataframe
    df_wo_line : pandas dataframe
    df_wo_pdx : pandas dataframe

    """
    # wt viability
    oneclass_input_wtviability = real_input.drop(columns=list_column_to_drop)
    # wo viability
    oneclass_input_woviability = oneclass_input_wtviability.drop(columns=['viability score'])
    # save files divided by origin
    df_wovia_line, df_wovia_pdx = save_df_origin(
        oneclass_input_woviability, which_class, result_dir, "wovia")
    
    return oneclass_input_woviability, df_wovia_line, df_wovia_pdx


def save_all_inputs(df, result_dir):
    """
    Obtain files with classN2, without viability (one for cell line and one for pdx)

    Parameters
    ----------
    df : pandas dataframe.
    result_dir : string.

    Returns
    -------
    None.

    """
    df_classn2_wovia, df_classn2_wovia_line, df_classn2_wovia_pdx=save_inputs(\
        df, ["3 classes encoded"], "2classes", result_dir)
     

def lag_final_data(x_id, y_id, variables_to_lag, other_vars, final_columns):
    """
    Function to lag data to adapt to tmiic input.

    Parameters
    ----------
    x_id : pandas dataframe. Dataframe corresponding to cell line data.
    y_id : pandas dataframe. Dataframe corresponding to PDX data.
    variables_to_lag : list of strings. Variables to lag.
    other_vars : list of strings. Variables to not lag.
    final_columns : list of strings. Final expected columns.

    Returns
    -------
    df_original : pandas dataframe. Concated dataframe before lagging.
    final_df : pandas dataframe.

    """
    # add Origin column
    x_id["Origin"] = "line"
    y_id["Origin"] = "pdx"
    # concatenate the two dataframes
    df_original = pd.concat([x_id, y_id])
    # melt the variables to lag
    melted_vars = []
    for single_var in variables_to_lag:
        value_vars = [single_var + f"_day{i}" for i in range(3)]
        melted_df = df_original.melt(id_vars='Unnamed: 0', 
                                   value_vars=value_vars, 
                                   var_name='day', 
                                   value_name=single_var)
        melted_df['day'] = melted_df['day'].str.extract('day(\d)').astype(int)
        melted_vars.append(melted_df)
    # concatenate 
    melted_df_lagged = pd.concat(melted_vars, axis=1)
    # replicate the other variables
    other_vars_df = df_original[other_vars].copy()
    other_vars_df = pd.concat([other_vars_df] * 3, ignore_index=True).sort_values(by=['UniqueIdentifier'])
    other_vars_df['ts'] = melted_df_lagged["day"].iloc[:,0]
    # concatenate melted lagged variables with the other variables 
    final_df = pd.concat([melted_df_lagged, other_vars_df], axis=1)
    # drop not necessary columns
    final_df = final_df.drop(columns=["day", "Unnamed: 0"])
    # reorder
    final_df=final_df.reindex(columns=final_columns)
    # keep viability, classes2 and classes 3 only at day 2
    # keep multiple_day0 and origin at day 0
    final_df.loc[final_df['ts'] != 2, 'viability score'] = np.nan
    final_df.loc[final_df['ts'] != 2, '2 classes encoded'] = np.nan
    final_df.loc[final_df['ts'] != 2, '3 classes encoded'] = np.nan
    final_df.loc[final_df['ts'] != 0, 'Origin'] = np.nan
    final_df.loc[final_df['ts'] != 1, 'Growth1-0'] = np.nan
    final_df.loc[final_df['ts'] != 2, 'Growth2-0'] = np.nan
    final_df.loc[final_df['ts'] != 2, 'Growth2-1'] = np.nan
    final_df.loc[final_df['ts'] != 1, 'Grey1-0'] = np.nan
    final_df.loc[final_df['ts'] != 2, 'Grey2-0'] = np.nan
    final_df.loc[final_df['ts'] != 2, 'Grey2-1'] = np.nan
    
    return df_original, final_df