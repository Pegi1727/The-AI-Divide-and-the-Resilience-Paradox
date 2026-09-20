# =====================================================================
# 01_data_cleaning_and_prep.R
# Data inspection, type checks, factor labelling, recoding & centering,
# integrity validation, and export of clean analysis-ready data.
#
# Inputs : AI_Resilience_Empirical_Dataset.xlsx (N = 60)
# Outputs: clean_ai_resilience.rds / .RData / .csv  + cleaning_log.csv
# Packages: readxl, dplyr, tidyr, janitor (optional), here-style paths
# =====================================================================

# ---- 0. Setup -------------------------------------------------------
pkgs <- c("readxl", "dplyr", "tidyr")
new  <- pkgs[!pkgs %in% rownames(installed.packages())]
if (length(new)) install.packages(new, quiet = TRUE)
invisible(lapply(pkgs, library, character.only = TRUE))

set.seed(1234)
data_path <- "AI_Resilience_Empirical_Dataset.xlsx"
out_dir   <- "."  # adjust (e.g., "data/clean") for your repo layout

cleaning_log <- list()

log_step <- function(step, msg) {
  cleaning_log[[length(cleaning_log) + 1]] <<- data.frame(step = step, note = msg)
  cat(sprintf("[%s] %s\n", step, msg))
}

# ---- 1. Load raw data -----------------------------------------------
dat <- readxl::read_excel(data_path)
log_step("LOAD", sprintf("Loaded %d rows x %d cols from %s",
                         nrow(dat), ncol(dat), data_path))

# ---- 2. Structural inspection ---------------------------------------
str(dat)
cat("\n-- Head --\n"); print(head(dat))
cat("\n-- Summary --\n"); print(summary(dat))

expected_vars <- c("ID", "Access_Plus", "Bank_Barrier", "Resilience",
                   "Motivation", "GPA", "Status")
stopifnot(all(expected_vars %in% names(dat)))
log_step("SCHEMA", "All 7 expected variables present.")

# Duplicate ID check
n_dup <- sum(duplicated(dat$ID))
if (n_dup > 0) warning(sprintf("%d duplicate IDs found!", n_dup))
log_step("DUPLICATES", sprintf("Duplicate IDs: %d", n_dup))

# ---- 3. Type enforcement --------------------------------------------
num_vars <- c("Access_Plus", "Bank_Barrier", "Resilience", "Motivation", "GPA")
dat <- dat %>%
  mutate(across(all_of(c(num_vars, "ID", "Status")), as.numeric))
log_step("TYPES", "Numeric coercion applied to all analysis variables.")

# ---- 4. Integrity / range validation --------------------------------
range_checks <- list(
  Access_Plus  = c(1, 5),
  Bank_Barrier = c(1, 5),
  Resilience   = c(1, 5),
  Motivation   = c(1, 5),
  GPA          = c(0, 100),
  Status       = c(1, 2)
)
violations <- vapply(names(range_checks), function(v) {
  rng <- range_checks[[v]]
  sum(dat[[v]] < rng[1] | dat[[v]] > rng[2], na.rm = TRUE)
}, numeric(1))
print(violations)
if (any(violations > 0)) warning("Range violations detected - inspect before analysis!")
log_step("RANGE", sprintf("Range violations per variable: %s",
                          paste(names(violations), violations, sep = "=", collapse = "; ")))

# Missing values
miss <- dat %>% summarise(across(everything(), ~ sum(is.na(.x))))
cat("\n-- Missing values per variable --\n"); print(miss)
log_step("MISSING", sprintf("Total NAs: %d", sum(unlist(miss))))

# ---- 5. Factor labelling --------------------------------------------
dat <- dat %>%
  mutate(
    # Status: 1 = Constrained/Restricted cohort, 2 = Seamless/semi-seamless cohort
    Status_f = factor(Status, levels = c(1, 2),
                      labels = c("Restricted_Access", "Seamless_Access")),
    # Cohort from continuous Access_Plus (Restricted <= 2; Seamless >= 4; 3 = Moderate)
    Access_Cohort = case_when(
      Access_Plus <= 2 ~ "Restricted",
      Access_Plus >= 4 ~ "Seamless",
      TRUE             ~ "Moderate"
    ),
    Access_Cohort = factor(Access_Cohort,
                           levels = c("Restricted", "Moderate", "Seamless")),
    Bank_Barrier_f = cut(Bank_Barrier, breaks = c(0, 2, 3, 5),
                         labels = c("Low", "Moderate", "High"))
  )
log_step("FACTORS", "Labelled Status_f, Access_Cohort (tiers), Bank_Barrier_f.")

# ---- 6. Recoded & centered variables --------------------------------
center_vars <- c("Access_Plus", "Bank_Barrier", "Resilience", "Motivation")
dat <- dat %>%
  mutate(
    # Mean-centered predictors (for interaction / moderation & SEM)
    Access_Plus_c  = Access_Plus  - mean(Access_Plus,  na.rm = TRUE),
    Bank_Barrier_c = Bank_Barrier - mean(Bank_Barrier, na.rm = TRUE),
    Resilience_c   = Resilience   - mean(Resilience,   na.rm = TRUE),
    Motivation_c   = Motivation   - mean(Motivation,   na.rm = TRUE),
    GPA_c          = GPA          - mean(GPA,          na.rm = TRUE),
    # Z-standardized versions
    across(all_of(center_vars), ~ as.numeric(scale(.x)),
           .names = "{.col}_z"),
    # Binary high/low split (median) as robustness variant
    Access_High = factor(Access_Plus >= median(Access_Plus),
                         levels = c(FALSE, TRUE),
                         labels = c("Low_Access", "High_Access"))
  )
log_step("CENTER", "Created *_c (mean-centered), *_z (standardized), Access_High.")

cat("\n-- Cleaned structure --\n"); str(dat)

# ---- 7. Export -------------------------------------------------------
write.csv(dat, file.path(out_dir, "clean_ai_resilience.csv"), row.names = FALSE)
saveRDS(dat, file.path(out_dir, "clean_ai_resilience.rds"))
save(dat, file = file.path(out_dir, "clean_ai_resilience.RData"))

log_df <- bind_rows(cleaning_log)
write.csv(log_df, file.path(out_dir, "cleaning_log.csv"), row.names = FALSE)

cat(sprintf("\nClean dataset (N = %d, %d variables) exported as:\n", nrow(dat), ncol(dat)))
cat(" - clean_ai_resilience.rds / clean_ai_resilience.RData / clean_ai_resilience.csv\n")
cat("Data preparation complete.\n")
