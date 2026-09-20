# =====================================================================
# 02_visualizations_publication.R
# Four publication-ready figures (300 DPI PNG + PDF) for the
# AI Access / Resilience / GPA study (N = 60).
#
# Requires: clean_ai_resilience.rds produced by 01_data_cleaning_and_prep.R
# Packages: ggplot2, ggpubr, patchwork, viridis, readxl (fallback)
# =====================================================================

# ---- 0. Setup -------------------------------------------------------
pkgs <- c("ggplot2", "ggpubr", "patchwork", "viridis", "dplyr", "readxl")
new  <- pkgs[!pkgs %in% rownames(installed.packages())]
if (length(new)) install.packages(new, quiet = TRUE)
invisible(lapply(pkgs, library, character.only = TRUE))

set.seed(1234)
fig_dir <- "figures"; if (!dir.exists(fig_dir)) dir.create(fig_dir)

theme_pub <- theme_minimal(base_size = 12) +
  theme(plot.title    = element_text(face = "bold", size = 12),
        plot.subtitle = element_text(size = 10),
        legend.position = "right",
        panel.grid.minor = element_blank())

save_fig <- function(p, name, w = 7, h = 5) {
  ggsave(file.path(fig_dir, paste0(name, ".png")), p,
         width = w, height = h, dpi = 300, bg = "white")
  ggsave(file.path(fig_dir, paste0(name, ".pdf")), p,
         width = w, height = h, device = cairo_pdf)
  cat("Saved:", name, "\n")
}

# ---- 1. Load data (clean RDS preferred, raw xlsx fallback) ----------
if (file.exists("clean_ai_resilience.rds")) {
  dat <- readRDS("clean_ai_resilience.rds")
} else {
  dat <- readxl::read_excel("AI_Resilience_Empirical_Dataset.xlsx")
  dat$Status_f <- factor(dat$Status, c(1, 2),
                         c("Restricted_Access", "Seamless_Access"))
  dat$Access_Cohort <- cut(dat$Access_Plus, c(0, 2, 3, 5),
                           c("Restricted", "Moderate", "Seamless"))
}
vars_core <- c("Access_Plus", "Bank_Barrier", "Resilience", "Motivation", "GPA")

# =====================================================================
# FIGURE 1: Correlation heatmap with coefficients and p-values
# =====================================================================
n_v <- length(vars_core)
cmat <- matrix(NA, n_v, n_v, dimnames = list(vars_core, vars_core))
pmat <- cmat
for (i in seq_len(n_v)) for (j in seq_len(n_v)) {
  ct <- suppressWarnings(cor.test(dat[[vars_core[i]]], dat[[vars_core[j]]]))
  cmat[i, j] <- unname(ct$estimate); pmat[i, j] <- unname(ct$p.value)
}
# Holm adjustment across the 10 unique pairs
pp <- pmat[upper.tri(pmat)]
pmat[upper.tri(pmat)] <- p.adjust(pp, method = "holm")
pmat[lower.tri(pmat)] <- t(pmat)[lower.tri(t(pmat))]

heat <- expand.grid(Var1 = vars_core, Var2 = vars_core, stringsAsFactors = FALSE)
heat$r <- cmat[cbind(heat$Var1, heat$Var2)]
heat$p <- pmat[cbind(heat$Var1, heat$Var2)]
heat$lab <- sprintf("%.2f%s", heat$r,
                    ifelse(heat$p < .001, "***",
                    ifelse(heat$p < .01,  "**",
                    ifelse(heat$p < .05,  "*", ""))))
heat$sig <- heat$p < .05

fig1 <- ggplot(heat, aes(Var2, Var1, fill = r)) +
  geom_tile(color = "white", linewidth = 1) +
  geom_text(aes(label = lab, color = sig), size = 3.6, fontface = "bold") +
  scale_color_manual(values = c(`TRUE` = "black", `FALSE` = "grey40"), guide = "none") +
  scale_fill_viridis_c(option = "mako", limits = c(-1, 1), name = "Pearson r") +
  labs(title = "Figure 1. Correlation matrix of core study variables",
       subtitle = "Cell values: Pearson r with Holm-adjusted significance (* p<.05, ** p<.01, *** p<.001)",
       x = NULL, y = NULL) +
  theme_pub + theme(axis.text.x = element_text(angle = 45, hjust = 1))
save_fig(fig1, "fig1_correlation_heatmap", 7, 5.5)

# =====================================================================
# FIGURE 2: Violin + box plots of GPA across Access tiers
# =====================================================================
fig2 <- ggplot(dat %>% dplyr::filter(!is.na(Access_Cohort)),
               aes(Access_Cohort, GPA, fill = Access_Cohort)) +
  geom_violin(alpha = .55, color = NA, trim = FALSE) +
  geom_boxplot(width = .18, outlier.shape = 21,
               outlier.size = 2.2, fill = "white", alpha = .9) +
  geom_jitter(width = .06, alpha = .45, size = 1.4, color = "grey25") +
  stat_summary(fun = mean, geom = "point", shape = 18, size = 3, color = "black") +
  scale_fill_viridis_d(option = "viridis", name = "Access Tier") +
  stat_compare_means(method = "kruskal.test",
                     label = "p = {p.format}", label.y = max(dat$GPA) + 2) +
  labs(title = "Figure 2. GPA across AI-access cohorts",
       subtitle = "Violin (distribution), box (IQR), diamond (M); points jittered; Kruskal-Wallis p",
       x = "AI Access Cohort", y = "Cumulative GPA (0-100)") +
  theme_pub
save_fig(fig2, "fig2_gpa_by_access_tier", 7, 5)

# =====================================================================
# FIGURE 3: Regression scatterplots with 95% CI bands (patchwork)
# =====================================================================
p_a <- ggplot(dat, aes(Motivation, GPA)) +
  geom_point(size = 2, alpha = .7, color = "grey30") +
  geom_smooth(method = "lm", level = .95, color = "#440154", fill = "#44015433") +
  stat_cor(method = "pearson", label.x = 1.1, label.y = max(dat$GPA)) +
  labs(title = "(a) Motivation -> GPA", x = "Academic Motivation (1-5)",
       y = "GPA (0-100)") + theme_pub

p_b <- ggplot(dat, aes(Access_Plus, GPA)) +
  geom_jitter(width = .15, size = 2, alpha = .7, color = "grey30") +
  geom_smooth(method = "lm", level = .95, color = "#21918c", fill = "#21918c33") +
  stat_cor(method = "pearson", label.x = 1.1, label.y = max(dat$GPA)) +
  labs(title = "(b) Access_Plus -> GPA", x = "Premium AI Access (1-5)",
       y = NULL) + theme_pub

fig3 <- (p_a | p_b) +
  plot_annotation(
    title = "Figure 3. OLS regressions with 95% confidence bands",
    theme = theme(plot.title = element_text(face = "bold", size = 12)))
save_fig(fig3, "fig3_regression_scatterplots", 9, 4.5)

# =====================================================================
# FIGURE 4: Path diagram for mediation (Bank_Barrier -> Motivation -> GPA)
# =====================================================================
# Single-mediator path model estimated with OLS (a, b, c', c paths)
m_a  <- lm(Motivation ~ Bank_Barrier, data = dat)   # a path
m_b  <- lm(GPA ~ Bank_Barrier + Motivation, data = dat)  # b & c' paths
m_c  <- lm(GPA ~ Bank_Barrier, data = dat)          # total effect c
a  <- coef(m_a)["Bank_Barrier"]
b  <- coef(m_b)["Motivation"]
cp <- coef(m_b)["Bank_Barrier"]
c  <- coef(m_c)["Bank_Barrier"]
ab <- a * b
# Sobel SE for the indirect effect
se_a <- summary(m_a)$coefficients["Bank_Barrier", "Std. Error"]
se_b <- summary(m_b)$coefficients["Motivation", "Std. Error"]
sobel_z <- ab / sqrt((a^2) * se_b^2 + (b^2) * se_a^2)
sobel_p <- 2 * pnorm(-abs(sobel_z))
fmt <- function(x, p) sprintf("%s = %.2f, p %s", x, p,
                              ifelse(p < .001, "< .001", sprintf("= %.3f", p)))
lab_a  <- sprintf("a: %s", fmt("b", summary(m_a)$coefficients["Bank_Barrier", "Pr(>|t|)"]))
lab_b  <- sprintf("b: %s", fmt("b", summary(m_b)$coefficients["Motivation", "Pr(>|t|)"]))
lab_cp <- sprintf("c': %s", fmt("b", summary(m_b)$coefficients["Bank_Barrier", "Pr(>|t|)"]))
lab_c  <- sprintf("c (total): %s", fmt("b", summary(m_c)$coefficients["Bank_Barrier", "Pr(>|t|)"]))
lab_ab <- sprintf("Indirect (a*b = %.2f): Sobel z = %.2f, p = %.4f", ab, sobel_z, sobel_p)

node <- function(x, y, label, fill) {
  annotate("rect", xmin = x - .22, xmax = x + .22, ymin = y - .09, ymax = y + .09,
           fill = fill, color = "grey25", linewidth = .7) +
  annotate("text", x = x, y = y, label = label, size = 3.4, fontface = "bold")
}

fig4 <- ggplot(NULL, aes(x = 0, y = 1)) + xlim(0, 1) + ylim(0, 1) +
  # paths
  annotate("segment", x = .30, y = .76, xend = .47, yend = .62,
           arrow = arrow(length = unit(.16, "cm"))) +
  annotate("segment", x = .53, y = .62, xend = .70, yend = .76,
           arrow = arrow(length = unit(.16, "cm"))) +
  annotate("segment", x = .30, y = .40, xend = .70, yend = .40,
           arrow = arrow(length = unit(.16, "cm"))) +
  # nodes
  node(.20, .30, "Bank_Barrier\n(structural friction)", "#5ec962") +
  node(.50, .72, "Motivation\n(pressure-driven)", "#440154") +
  node(.80, .30, "GPA\n(academic outcome)", "#31688e") +
  # labels
  annotate("text", x = .32, y = .70, label = lab_a, size = 3.1, hjust = 1) +
  annotate("text", x = .68, y = .70, label = lab_b, size = 3.1, hjust = 0) +
  annotate("text", x = .50, y = .33, label = lab_cp, size = 3.1) +
  annotate("text", x = .50, y = .12, label = lab_c,  size = 3.1) +
  annotate("text", x = .50, y = .04, label = lab_ab, size = 3.1, fontface = "italic") +
  labs(title = "Figure 4. Mediation path model: Bank_Barrier -> Motivation -> GPA",
       subtitle = "Unstandardized OLS coefficients (N = 60); N = 60") +
  theme_void(base_size = 12) +
  theme(plot.title = element_text(face = "bold", size = 12),
        plot.subtitle = element_text(size = 10))
save_fig(fig4, "fig4_mediation_path_diagram", 8, 5.5)

cat("All 4 figures saved to '", fig_dir, "/' as PNG (300 DPI) and PDF.\n", sep = "")
