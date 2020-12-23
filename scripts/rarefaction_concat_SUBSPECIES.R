# Load packages -----------------------------------------------------------

library(tidyverse)

# Rarefaction curves of Kraken rarefaction (Waffles) ----------------------

# Microbiome rarefaction data generated in NML cluster (Waffles)

krakenRarWaffles <- unlist(snakemake@input)

# Extract sample names from list of files names
krakenRarWafflesFileNames <- basename(krakenRarWaffles)

rarCategories <- c("Rates", 
                   "Reads", 
                   "Domains", 
                   "Phyla", 
                   "Classes", 
                   "Orders", 
                   "Families", 
                   "Genera", 
                   "Species",
                   "Subspecies")

# Created named list (similar to dictionary). 
# Names (or keys) are the sample names extracted above in krakenRarWafflesFileNames
# Values are the data frames
# Read CSV files, transpose, assign column names to each data frame
# Then assign sample names to each data frame

krakenRarWafflesAll <- map(krakenRarWaffles, function(x){
  df <- read.csv(x, header=FALSE)
  df <- t(df)
  colnames(df) = rarCategories
  df <- df[2:nrow(df),]
  as.data.frame(df)
}) %>%
  set_names(nm=krakenRarWafflesFileNames)

# Join all of the data frames into one. Use the name (or key) of each data frame and put it in a new column called "Sample"
krakenRarWafflesDF <- bind_rows(krakenRarWafflesAll, .id = "Sample")

# Might Need to enforce numeric type of most of the rates and counts columns

krakenRarWafflesDF$Rates <- as.numeric(as.character(krakenRarWafflesDF$Rates))
krakenRarWafflesDF$Reads <- as.numeric(as.character(krakenRarWafflesDF$Reads))
krakenRarWafflesDF$Domains <- as.numeric(as.character(krakenRarWafflesDF$Domains))
krakenRarWafflesDF$Phyla <- as.numeric(as.character(krakenRarWafflesDF$Phyla))
krakenRarWafflesDF$Classes <- as.numeric(as.character(krakenRarWafflesDF$Classes))
krakenRarWafflesDF$Orders <- as.numeric(as.character(krakenRarWafflesDF$Orders))
krakenRarWafflesDF$Families <- as.numeric(as.character(krakenRarWafflesDF$Families))
krakenRarWafflesDF$Genera <- as.numeric(as.character(krakenRarWafflesDF$Genera))
krakenRarWafflesDF$Species <- as.numeric(as.character(krakenRarWafflesDF$Species))
krakenRarWafflesDF$Subspecies <- as.numeric(as.character(krakenRarWafflesDF$Subspecies))

#krakenRarWafflesDF$Sample <- as.factor(krakenRarWafflesDF$Sample)

# Reshaping dataframe to tidy or long format (variables as columsn, observations as rows)
# Probably should update to tidyr::pivot_longer
krakenRarWafflesTidy <- krakenRarWafflesDF %>%
  tidyr::gather(key = Level, value = taxonCount, -Sample,-Rates,-Reads)

write.csv(krakenRarWafflesTidy, file.path(getwd(), 'results/results_concat.csv'), row.names = FALSE, quote = FALSE)

