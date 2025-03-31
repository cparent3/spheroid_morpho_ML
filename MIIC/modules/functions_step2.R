# Functions

# Select columns
choose_correct_columns <- function(name_id, col_to_remove){
  
  if (name_id=="recompute"){
    columns_to_delete <- c("multiple", "Experiment.ID", "drug.concentration..uM.", "spheroIndex", "UniqueIdentifier")
    columns_new_names <- c("Area"="Area..pix2.", "Perimeter"="Perimeter..pix.",
                           "EqDiameter" = "Equivalent.Diameter..pix.",
                           "MeanGreyValue"="Mean.grey.value",
                           "Viability"="viability.score",
                           "ClassN2"="X2.classes.encoded",
                           "ClassN3"="X3.classes.encoded",
                           "NumSpheroidsDay0"="multiple_day0")
  } else if (name_id=="original"){
    columns_to_delete <- c("Experiment.ID", "drug.concentration..uM.", "spheroIndex", "UniqueIdentifier")
    columns_new_names <- c("Area"="Area..um2.", "Perimeter"="Perimeter..um.",
                           "EqDiameter" = "Equivalent.Diameter..um.",
                           "MeanGreyValue"="Mean.grey.value",
                           "Viability"="viability.score",
                           "ClassN2"="X2.classes.encoded",
                           "ClassN3"="X3.classes.encoded"
    )}
    else if (name_id=="merged"){
      columns_to_delete <- c("Experiment.ID", "drug.concentration..uM.", "spheroIndex", "UniqueIdentifier",
                             "final_id")
      columns_new_names <- c("Area"="Area..um2.", "Perimeter"="Perimeter..um.",
                             "EqDiameter" = "Equivalent.Diameter..um.",
                             "MeanGreyValue"="Mean.grey.value",
                             "Viability"="viability.score",
                             "ClassN2"="X2.classes.encoded",
                             "ClassN3"="X3.classes.encoded",
                             "NumSpheroidsDay0"="multiple_day0"
      )}
    else if (name_id=="merged_wt_concentration"){
        columns_to_delete <- c("Experiment.ID", "spheroIndex", "UniqueIdentifier",
                               "final_id")
        columns_new_names <- c("Area"="Area..um2.", "Perimeter"="Perimeter..um.",
                               "EqDiameter" = "Equivalent.Diameter..um.",
                               "MeanGreyValue"="Mean.grey.value",
                               "Viability"="viability.score",
                               "ClassN2"="X2.classes.encoded",
                               "ClassN3"="X3.classes.encoded",
                               "NumSpheroidsDay0"="multiple_day0",
                               "Concentration"="drug.concentration..uM."
      )
  } else {print("Issue with name_id")}
  
  if (!is.null(col_to_remove)){
    columns_new_names <- columns_new_names[!names(columns_new_names) %in% col_to_remove]
    print(sprintf("%s removed", col_to_remove))
    
  } else {
    print("No columns were removed.")
  }
  
  output_list <- list("columns_to_delete" = columns_to_delete, "columns_new_names" = columns_new_names)
}

# Preprocess dataframe
preprocess_dataframe <- function(df, columns_to_delete, columns_new_names){
  # datatypes
  # order
  df <- df %>% arrange(UniqueIdentifier, ts)
  # delete the columns
  df_input <- df[,!names(df) %in% columns_to_delete]
  # convert names of some columns
  df_input <- df_input %>% rename(!!!columns_new_names)
  df_input["ts"] <- df_input["ts"]+1 # it must start with 1
  # if concentration is in the dataframe, then keep the value only for ts=1
  if ("Concentration" %in% colnames(df_input)){
    df_input <- df_input %>%
      mutate(Concentration = ifelse(ts != 1, NA, Concentration))}
  return (df_input)
}

# Find names lagged variables
find_names_lagged_variables <- function(df_input, n_frames){
  tMIIC_df <- df_input[,!names(df_input) %in% "ts"]
  name_variables <- colnames(tMIIC_df)
  complete_names <- c()
  
  n_row<-1
  for (i in 1:n_frames){
    for (j in 1:length(name_variables)){
      i_true = i-1
      if (i_true == 0)
        addition <- sprintf("_lag%s", i_true)
      else
        addition <- sprintf("_lag+%s", i_true)
      complete_names[n_row] <- (paste0(name_variables[j], addition))
      n_row <- n_row+1
    }
  }
  return(complete_names)
}

# Create layout
create_layout_temporal <- function(df_input, n_frames=3, nodesize=20, edgelength=100){
  # find names of lagged variables
  complete_names <- find_names_lagged_variables(df_input, n_frames)
  network_layout <- list(nodeLabelSize= nodesize, threshold = c(0), edgeLength = edgelength, savedPositions = list())
  #Generate list of coordinates
  tmp_list <- vector(mode="list", length = length(complete_names))
  names(tmp_list) <- complete_names
  # parameters
  n_to_use <- ncol(df_input[,!names(df_input) %in% "ts"]) # variables
  extrem_x <- -(n_to_use-1)*100
  extrem_y <- 0
  pas <- 100
  nb_var <- n_to_use
  
  for (i in 1:length(complete_names)) {
    tmp_list[[complete_names[i]]] <- c(extrem_x + (i-1)%%nb_var*pas , extrem_y + ((i-1)%/%nb_var*pas))
  }
  #names(tmp_list)<- gsub("\\.", "-", colnames(tMIIC_df))
  network_layout[["savedPositions"]] <- tmp_list
  
  return(network_layout)
}


# Run tsnmiic
pipeline_tnsmiic <- function(name_id, filename, filename_save, flag_layout,nlayers=3,
                             deltat=1, nframes=3, col_to_remove=NULL){
  # choose correct columns
  output <- choose_correct_columns(name_id, col_to_remove)
  columns_to_delete <- output[["columns_to_delete"]]
  columns_new_names <- output[["columns_new_names"]]
  # load file
  df <- read.csv(sprintf("results/%s.csv", filename))
  # process data
  df_input <- preprocess_dataframe(df, columns_to_delete, columns_new_names)
  # miic tns
  res <- miic(df_input, mode="TNS", n_layers=nlayers, delta_t=deltat)
  
  # save summary and orientations and lagged file and state order as .tsv
  dt <- format(as.Date(Sys.time(), format="%Y%m%d"), "%Y%m%d")
  summary <- res$all.edges.summary
  write.table(summary, sprintf("results/%s_%s_summary.tsv", dt, filename_save), sep='\t', quote=FALSE,row.names = FALSE)
  write.table(res$orientations.prob, sprintf("results/%s_%s_orientations.tsv", dt, filename_save), sep='\t', quote=FALSE,row.names = FALSE)
  write.table(res$tmiic$lagged_input_data, sprintf("results/%s_%s_processed.tsv", dt, filename_save), sep='\t', quote=FALSE,row.names = FALSE)
  write.table(res$tmiic$lagged_state_order, sprintf("results/%s_%s_stateorder.tsv", dt, filename_save), sep='\t', quote=FALSE,row.names = FALSE)
  
  # network layout and save
  if (flag_layout){
    network_layout <- create_layout_temporal(df_input, n_frames=nframes, nodesize=20, edgelength=100)
    json <- rjson::toJSON(network_layout)
    file <- file(sprintf("Layout/%s_%s_temporaldata.json", dt, filename_save))
    writeLines(json, file)
    close(file)}
  
  output_list <- list("df"=df, "df_input"=df_input, "res"=res)
  return(output_list)
}


