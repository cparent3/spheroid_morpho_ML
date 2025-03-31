# Code to obtain MIIC networks.
library(miic)
library(rjson) 
library(tidyverse)
setwd("/Users/tizia/Desktop/Spheroids GitHub/MIIC")
source("modules/functions_step2.R")

# One network for Cell line and one network for PDX
name_id <- "original"
output_line <- pipeline_tnsmiic(
  name_id, "inputmiictns_2classes_wovia_line", 
  "outputmiictns_2classes_wovia_line", 
  flag_layout=0, col_to_remove=c("ClassN3", "Viability"))
output_pdx <- pipeline_tnsmiic(
  name_id, "inputmiictns_2classes_wovia_pdx", 
  "outputtmiictns_2classes_wovia_pdx", 
  flag_layout=0, col_to_remove=c("ClassN3", "Viability"))

