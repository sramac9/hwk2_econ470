## Author:        Sammy Ramacher
## Date Created:  2/18/2025
## Date Edited:   2/18/2025

if (!require("pacman")) install.packages("pacman")
pacman::p_load(tidyverse, ggplot2, dplyr, lubridate, flextable)
library(dplyr)
library(lubridate)  # For `mdy()`


#source("submission2/data-code/_HCRIS_Data.R")
#data=read_rds("data/output/full_HCRIS_Data.rds")


#question 1
final.hcris.v1996=read_csv("data/output/HCRIS_v1996.csv")
final.hcris.v2010=read_csv("data/output/HCRIS_v2010.csv")


    ## create missing variables for columns introduced in v2010 of hcris forms
final.hcris.v1996 = final.hcris.v1996 %>%
  mutate(hvbp_payment=NA, hrrp_payment=NA)

    ## combine v1996 and v2010 hcris forms, and sort by provider_number/year
final.hcris <- rbind(final.hcris.v1996, final.hcris.v2010) %>%
  mutate(fy_end=mdy(fy_end),fy_start=mdy(fy_start),
         date_processed=mdy(date_processed),date_created=mdy(date_created),
         tot_discounts=abs(tot_discounts), hrrp_payment=abs(hrrp_payment)) %>%
  mutate(fyear=year(fy_end)) %>%
  arrange(provider_number,fyear)

final.hcris =
  final.hcris %>% 
  add_count(provider_number, fyear, name="total_reports")
duplicate.hcris = 
  final.hcris %>%
  filter(total_reports>1) %>%
  mutate(time_diff=fy_end-fy_start)

report_counts <- duplicate.hcris %>%
  group_by(fyear) %>%
  summarise(num_hospitals = n_distinct(provider_number))

## creating a line graph
#ggplot(report_counts, aes(x = fyear, y = num_hospitals)) +
    #geom_line() +
    #labs(title = "Number of Hospitals Over Time",
             #x = "Fiscal Year",
             #y = "Number of Hospitals") +
    #theme_minimal()
hospitals_per_year <- duplicate.hcris %>% group_by(year) %>% summarise(num_hospitals =n_distinct(provider_number), .groups = 'drop') 
table0 = ggplot(hospitals_per_year, aes(x = year,y = num_hospitals)) + geom_line() + geom_point() + labs(title = "Number of Hospitals Filing More Than One Report Per Year", x = "Year", y = "Number of Hospitals") + theme_minimal() + theme(axis.text.x = element_text(angle = 45, hjust =1))
ggsave("my_plot.png", plot = table0, width = 8, height = 6, dpi = 300, bg = "white")




#Question 2
data=read_rds("data/output/full_HCRIS_Data.rds")
unique_counts <- data %>%
  group_by(year) %>%
  summarise(num_unique_providers = n_distinct(provider_number), .groups = 'drop')


library(flextable)

# Create a nice table
table <- unique_counts %>%
  flextable() %>%
  set_caption("Unique Providers Per Year") %>%
  theme_vanilla() %>%
  bg(part = "all", bg = "white") %>%
  set_table_properties(width = 1, layout = "autofit") %>% # Auto-fit columns
  font(fontname = "Arial") %>% # Set a nice readable font
  align(align = "center", part = "all") # Center text

# Save as PNG
install.packages("webshot2") # Install webshot2 for saving images
library("webshot2")
#save_as_image(table, path = "unique_providers_per_year.png")

#Question 3
ggplot(final.hcris.data, aes(x = fyear, y = log(tot_charges))) + geom_violin(fill = "lightblue", color = "darkblue") + labs(title = "Log-transformed Distribution of Total Charges by Year", x = "Year", y = "Log of Total Charges" ) +theme_minimal() + theme(axis.text.x = element_text(angle = 45, hjust = 1))

