## Author:        Sammy Ramacher
## Date Created:  2/18/2025
## Date Edited:   2/18/2025

if (!require("pacman")) install.packages("pacman")
pacman::p_load(tidyverse, ggplot2, dplyr, lubridate, flextable)
library(dplyr)
library(lubridate)  # For `mdy()`
library(knitr)

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
#ggsave("Q1.png", plot = table0, width = 6, height = 5, dpi = 300, bg = "white")




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

#Question 4
data$fyear <- as.factor(data$year)
table3 = ggplot(data, aes(x = fyear, y = log(tot_charges))) + geom_violin(fill = "lightblue", color = "darkblue") + labs(title = "Log-transformed Distribution of Total Charges by Year", x = "Year", y = "Log of Total Charges" ) +theme_minimal() + theme(axis.text.x = element_text(angle = 45, hjust = 1))
#ggsave("Q3.png", plot = table3, width = 6, height = 5, dpi = 300, bg = "white")

data <- data %>%
  mutate(discount_factor = 1 - tot_discounts / tot_charges)

data <- data %>%
  mutate(price_num = (ip_charges + icu_charges + ancillary_charges) * discount_factor - tot_mcare_payment)

data <- data %>%
  mutate(price_denom = tot_discharges - mcare_discharges)

data <- data %>%
  mutate(price = price_num / price_denom)

quantiles <- quantile(data$price, c(0.01, 0.99), na.rm = TRUE)
data <- data %>%
  filter(price >= quantiles[1], price <= quantiles[2])

data$fyear <- as.factor(data$fyear)

table4 = ggplot(data, aes(x = fyear, y = price)) +
  geom_violin(fill = "lightblue", color = "darkblue") +  
  labs(
    title = "Distribution of Estimated Prices by Year",
    x = "Year",
    y = "Estimated Price"
  ) +
  theme_minimal() +  
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
#ggsave("Q4.png", plot = table4, width = 6, height = 5, dpi = 300, bg = "white")

#Question 5
# Question 5: 
## Filter for 2012 and define penalty
final.hcris.2012 <- data %>%
    ungroup() %>%
    filter(
        price_denom > 100, !is.na(price_denom),
        price_num > 0, !is.na(price_num),
        price < 100000,
        beds > 30,
        year == 2012
    ) %>%
    mutate(
        hvbp_payment = ifelse(is.na(hvbp_payment), 0, hvbp_payment),
        hrrp_payment = ifelse(is.na(hrrp_payment), 0, abs(hrrp_payment)),
        penalty = (hvbp_payment - hrrp_payment) < 0  # TRUE/FALSE
    )
## Calculate mean prices for penalized vs non-penalized hospitals
mean.pen <- round(mean(final.hcris.2012$price[final.hcris.2012$penalty == TRUE], na.rm = TRUE), 2)
mean.nopen <- round(mean(final.hcris.2012$price[final.hcris.2012$penalty == FALSE], na.rm = TRUE), 2)

## Print results
cat("Mean price for penalized hospitals:", mean.pen, "\n")
cat("Mean price for non-penalized hospitals:", mean.nopen, "\n")

# Print results as a table
results <- data.frame(
    Category = c("Penalized Hospitals", "Non-Penalized Hospitals"),
    Mean_Price = c(mean.pen, mean.nopen)
)
print(results)


#Question 6
# Question 6: Hospitals into quartiles
## Define penalty: HVBP + HRRP < 0
final.hcris.2012 <- data %>%
    mutate(
        hvbp_payment = ifelse(is.na(hvbp_payment), 0, hvbp_payment),
        hrrp_payment = ifelse(is.na(hrrp_payment), 0, hrrp_payment),
        penalty = (hvbp_payment + hrrp_payment) < 0
    )
## Calculate bed size quartiles
bed_quartiles <- quantile(final.hcris.2012$beds, probs = c(0.25, 0.50, 0.75), na.rm = TRUE)

## Assign each hospital to a bed size quartile
final.hcris.2012 <- final.hcris.2012 %>%
  mutate(
    Q1 = as.numeric((beds <= bed_quartiles[1]) & (beds > 0)),
    Q2 = as.numeric((beds > bed_quartiles[1]) & (beds <= bed_quartiles[2])),
    Q3 = as.numeric((beds > bed_quartiles[2]) & (beds <= bed_quartiles[3])),
    Q4 = as.numeric(beds > bed_quartiles[3])
  )

## Calculate average prices by quartile and penalty status
quartile_summary <- final.hcris.2012 %>%
  mutate(bed_quartile = case_when(
    Q1 == 1 ~ "Q1",
    Q2 == 1 ~ "Q2",
    Q3 == 1 ~ "Q3",
    Q4 == 1 ~ "Q4"
  )) %>%
  group_by(bed_quartile, penalty) %>%
  summarise(avg_price = mean(price, na.rm = TRUE), .groups = "drop") %>%
  pivot_wider(names_from = penalty, values_from = avg_price, names_prefix = "penalty_")

## Print the table
#print(quartile_summary)

library(ggplot2)
library(gridExtra)
library(grid)

# Create a table plot
table_plot <- tableGrob(quartile_summary)

# Save the table as a PNG
#ggsave("Q6.png", plot = table_plot, width = 6, height = 4, dpi = 300)


#Question 7
# Question 7: Average Treatment Effects
install.packages("Matching")
install.packages("MatchIt")
install.packages("WeightIt")

## Nearest neighbor matching (1-to-1) with inverse variance distance based on quartiles of bed size
lp.covs <- final.hcris.2012 %>%
  select(Q1, Q2, Q3, Q4) %>%
  na.omit()

lp.vars <- final.hcris.2012 %>%
  select(price, penalty) %>%
  na.omit()

m.nn.var <- Matching::Match(Y=lp.vars$price,
                            Tr=lp.vars$penalty,
                            X=lp.covs,
                            M=1, 
                            Weight=1,
                            estimand="ATE")

ate_nn_var <- m.nn.var$est
se_nn_var <- m.nn.var$se

# Nearest neighbor matching with Mahalanobis distance
m.nn.md <- Matching::Match(Y = lp.vars$price,
                            Tr = lp.vars$penalty,
                            X = lp.covs,
                            M = 1,
                            Weight = 2,
                            estimand = "ATE")

ate_nn_md <- m.nn.md$est
se_nn_md <- m.nn.md$se

# Inverse propensity weighting
logit.model <- glm(penalty ~ Q1 + Q2 + Q3 + Q4, family = binomial, data = final.hcris.2012)
ps <- fitted(logit.model)
ipw_weights <- ifelse(final.hcris.2012$penalty == 1, 1 / ps, 1 / (1 - ps))
ate_ipw <- weighted.mean(lp.vars$price, ipw_weights)

# Simple linear regression
final.hcris.2012$Q1_interaction <- final.hcris.2012$penalty * final.hcris.2012$Q1
final.hcris.2012$Q2_interaction <- final.hcris.2012$penalty * final.hcris.2012$Q2
final.hcris.2012$Q3_interaction <- final.hcris.2012$penalty * final.hcris.2012$Q3
final.hcris.2012$Q4_interaction <- final.hcris.2012$penalty * final.hcris.2012$Q4

lm_model <- lm(price ~ penalty + Q1 + Q2 + Q3 + Q4 + 
                 Q1_interaction + Q2_interaction + Q3_interaction + Q4_interaction, 
               data = final.hcris.2012)

ate_lm <- coef(lm_model)["penalty"]

# Combine results into a table
q7 <- data.frame(
  Method = c("Nearest Neighbor Matching (IV)", "Nearest Neighbor Matching (Mahalanobis)", 
             "Inverse Propensity Weighting", "Simple Linear Regression"),
  ATE = c(ate_nn_var, ate_nn_md, ate_ipw, ate_lm),
  SE = c(se_nn_var, se_nn_md, NA, summary(lm_model)$coefficients["penaltyTRUE", "Std. Error"]))

print(q7)
ggsave("Q7.png", plot = q7, width = 6, height = 4, dpi = 300)

#save.image("submission2/Hwk2_workspace.Rdata")