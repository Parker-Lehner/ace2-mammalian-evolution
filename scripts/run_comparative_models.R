#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(ape)
  library(nlme)
})

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
traits_path <- file.path(root, "data", "processed", "mammal_ecology_traits_curated.tsv")
metrics_path <- file.path(root, "data", "processed", "ace2_evolutionary_metrics.tsv")
out_path <- file.path(root, "results", "models", "comparative_model_summary.tsv")

if (!file.exists(traits_path)) {
  stop("Missing curated traits: ", traits_path)
}
if (!file.exists(metrics_path)) {
  stop("Missing ACE2 metrics: ", metrics_path)
}

traits <- read.delim(traits_path, stringsAsFactors = FALSE)
metrics <- read.delim(metrics_path, stringsAsFactors = FALSE)
dat <- merge(metrics, traits, by = "scientific_name")

dir.create(dirname(out_path), recursive = TRUE, showWarnings = FALSE)

candidate_predictors <- c("habitat_class", "diving_class", "max_dive_depth_m", "max_dive_duration_min", "foraging_depth_m", "body_mass_kg")
candidate_responses <- setdiff(names(metrics), "scientific_name")

rows <- list()
for (response in candidate_responses) {
  for (predictor in candidate_predictors) {
    model_dat <- dat[, c(response, predictor)]
    model_dat <- model_dat[complete.cases(model_dat), ]
    if (nrow(model_dat) < 20) next
    formula <- as.formula(paste(response, "~", predictor))
    fit <- lm(formula, data = model_dat)
    sm <- summary(fit)
    rows[[length(rows) + 1]] <- data.frame(
      response = response,
      predictor = predictor,
      n = nrow(model_dat),
      r_squared = sm$r.squared,
      p_value_model = pf(sm$fstatistic[1], sm$fstatistic[2], sm$fstatistic[3], lower.tail = FALSE)
    )
  }
}

if (length(rows) == 0) {
  writeLines("response\tpredictor\tn\tr_squared\tp_value_model", out_path)
} else {
  write.table(do.call(rbind, rows), out_path, sep = "\t", row.names = FALSE, quote = FALSE)
}

message("Wrote ", out_path)
