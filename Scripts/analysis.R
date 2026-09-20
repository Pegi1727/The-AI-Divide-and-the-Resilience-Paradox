# =====================================================================
# analysis.R
# Replication analysis: AI access, resilience, motivation, barriers, GPA
# Self-contained, reproducible script (set.seed fixed)
# Packages: readxl, tidyverse, psych, car, mediation, ggplot2, gridExtra
# =====================================================================

# ---- 0. Setup -------------------------------------------------------
pkgs <- c("readxl","tidyverse","psych","car","mediation","ggplot2","gridExtra")
new  <- pkgs[!pkgs %in% installed.packages()[, "Package"]]
if (length(new)) install.packages(new, quiet = TRUE)
invisible(lapply(pkgs, library, character.only = TRUE))

set.seed(1234)  # reproducibility (mediation bootstrap)

# ---- 1. Load data ---------------------------------------------------
data_path <- "AI_Resilience_Empirical_Dataset.xlsx"  # adjust if needed
dat <- read_excel(data_path) %>%
  mutate(across(where(is.numeric), as.numeric))

cat("Dimensions:", dim(dat), "\n")
glimpse(dat)

# ---- 2. Descriptive statistics --------------------------------------
desc <- describe(dat[, c("Access_Plus","Bank_Barrier","Resilience",
                         "Motivation","GPA")])
print(desc)
round(cor(dat %>% select(-ID, -Status), use = "pairwise"), 3)
print(cor.plot(dat %>% select(-ID, -Status), numbers = TRUE))

# ---- 3. Full model + assumption checks ------------------------------
fit_full <- lm(Resilience ~ Access_Plus + Motivation + Bank_Barrier, data = dat)
summary(fit_full)

shapiro.test(residuals(fit_full))   # normality of residuals
car::ncvTest(fit_full)              # homoscedasticity
car::vif(fit_full)                  # multicollinearity

# ---- 4. Regression models (mediation paths) -------------------------
m1 <- lm(Resilience ~ Access_Plus, data = dat)    # total effect (c)
m2 <- lm(Motivation ~ Access_Plus, data = dat)    # a path
m3 <- lm(Resilience ~ Access_Plus + Motivation + Bank_Barrier,
         data = dat)                              # b and c-prime paths
summary(m1); summary(m2); summary(m3)

# APA-style coefficient table helper
apa_lm <- function(model) {
  s <- summary(model)$coefficients
  data.frame(term = rownames(s), b = s[, "Estimate"],
             se = s[, "Std. Error"], t = s[, "t value"],
             p = s[, "Pr(>|t|)"], row.names = NULL)
}
knitr::kable(apa_lm(m1), digits = 3)
knitr::kable(apa_lm(m2), digits = 3)
knitr::kable(apa_lm(m3), digits = 3)

# ---- 5. ANOVA: resilience by status group ---------------------------
dat$Status_f <- factor(dat$Status, levels = c(1, 2),
                       labels = c("Group1", "Group2"))
fit_aov <- aov(Resilience ~ Status_f, data = dat)
summary(fit_aov)
s <- summary(fit_aov)[[1]]
eta2 <- s[1, "Sum Sq"] / (s[1, "Sum Sq"] + s[2, "Sum Sq"])
cat("eta-squared (Status):", round(eta2, 3), "\n")

# ---- 6. Mediation analysis ------------------------------------------
set.seed(1234)
med_fit <- mediate(m2, m3, treat = "Access_Plus", mediator = "Motivation",
                   boot = TRUE, sims = 1000)
summary(med_fit)
plot(med_fit)

# ---- 7. Plots -------------------------------------------------------
p1 <- ggplot(dat, aes(Access_Plus, Resilience)) +
  geom_jitter(width = 0.15, alpha = 0.6) +
  geom_smooth(method = "lm") +
  labs(x = "AI Access (Access_Plus)", y = "Resilience",
       title = "Access Predicting Resilience") +
  theme_minimal()

p2 <- ggplot(dat, aes(Motivation, Resilience, color = Status_f)) +
  geom_jitter(width = 0.15, alpha = 0.6) +
  geom_smooth(method = "lm", se = FALSE) +
  labs(x = "Motivation", y = "Resilience", color = "Status") +
  theme_minimal()

grid.arrange(p1, p2, ncol = 2)
ggsave("fig1_access_resilience.png", p1, width = 6, height = 4, dpi = 300)
ggsave("fig2_motivation_resilience.png", p2, width = 6, height = 4, dpi = 300)

cat("Analysis complete.\n")
