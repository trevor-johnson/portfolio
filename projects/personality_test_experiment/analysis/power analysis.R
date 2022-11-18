libraries <- c("tidyverse", "data.table")
sapply(libraries, require, character.only = T)

# factor 1 - extroversion
# factor 2 - emotional stability
# factor 3 - agreeableness 
# factor 4 - conscientiousness
# factor 5 - intellect/imagination



# function to run one power test
# i run a regression on each factor individually
# recommended to set the alpha to .05/5 for bonferonni adjustment
power_analysis_one_test <- function(samp_size = 50, treatment_split = .5, 
                                    force_even_split = T, tau = -5, factor_mean = 50, 
                                    factor_sd = 10, alpha = .01){
  
  # sample ppl and put them into treatment or control. Depends on if we want even splits or not
  if (force_even_split){
    df <- data.table(condition = c(rep("treatment", round(samp_size/2,0)), rep("control", round(samp_size/2,0))))
  }else{
    df <- data.table(condition = sample(c("treatment", "control"), size = samp_size, replace = T))
  }
  
  # now sample from the normal distribution to assign the treatment effect. 
  # if they are in treatment, they get the added "tau" effect. 
  # control just gets rnrom()
  for (i in 1:5){
    df[, paste0("factor", i) := ifelse(condition == "treatment", 
                                       rnorm(nrow(df[condition == "treatment",]), factor_mean + tau, factor_sd),
                                       rnorm(nrow(df[condition == "control",]), factor_mean, factor_sd)
    )]
  }
  
  # finally, calculate p-value for every personality factor
  pvals <- c()
  for (i in 1:5){
    fit <- summary(lm(as.formula(paste0("factor", i, "~ condition")), data = df))
    pval <- fit$coefficients[2,4]
    pvals <- c(pvals, pval)
  }
  
  # are any of them significant?
  sig <- sum(pvals < alpha) > 0
  
  # return boolean for if it's significant or not
  return(sig)
  
}

# can run this one time and it returns a T/F if you found any sort of significance in any of the factors
power_analysis_one_test(samp_size = 10, treatment_split = .5, force_even_split = T, tau = -5, factor_mean = 50, factor_sd = 10)

# showing how we can repeatedly run the experiment a thousand times and calculate the mean number of times we find significance.
set.seed(1)
trials1 <- sapply(1:1000, 
                  function(x) power_analysis_one_test(
                    samp_size = 100, treatment_split = .5, force_even_split = T, 
                    tau = -5, factor_mean = 50, factor_sd = 10))
mean(trials1) # .13





# Changing the sample size and running the experiment 1,000 times at various sample sizes and calculating the power. 
adjust_sample_size <- function(samp_sizes, iter=1000){
  
  output_samp_size <- c()
  for (i in samp_sizes){
    output_samp_size <- c(output_samp_size, 
                          mean(sapply(1:iter, function(x) power_analysis_one_test(
                            samp_size = i, treatment_split = .5, force_even_split = T, 
                            tau = 7, factor_mean = 50, factor_sd = 15))))
    print(paste0("Sample size ", i, " done."))
  }
  
  df_out <- data.table(
    sample_size = samp_sizes,
    power = output_samp_size
  )
  
  return(df_out)
}

set.seed(1)
df1 <- adjust_sample_size(c(seq(10, 100, 10), 150, 200), iter=100)

# plot
df1 %>% 
  ggplot(aes(x = sample_size, y = power)) + 
  geom_line() + 
  labs(title = "Power as Sample Size Increases", y = "Power", x = "Sample Size") +
  theme_minimal()





#####
# again w/ some diff params
adjust_sample_size <- function(samp_sizes, iter=1000){
  
  output_samp_size <- c()
  for (i in samp_sizes){
    output_samp_size <- c(output_samp_size, 
                          mean(sapply(1:iter, function(x) power_analysis_one_test(
                            samp_size = i, treatment_split = .5, force_even_split = T, 
                            tau = 3, factor_mean = 50, factor_sd = 15))))
    print(paste0("Sample size ", i, " done."))
  }
  
  df_out <- data.table(
    sample_size = samp_sizes,
    power = output_samp_size
  )
  
  return(df_out)
}

set.seed(1)
df1 <- adjust_sample_size(seq(50, 500, 50), iter=300)

# plot
df1 %>% 
  ggplot(aes(x = sample_size, y = power)) + 
  geom_line() + 
  labs(title = "Power as Sample Size Increases", y = "Power", x = "Sample Size") +
  theme_minimal()







