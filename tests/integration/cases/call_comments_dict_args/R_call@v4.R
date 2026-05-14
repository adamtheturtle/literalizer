process <- function(...) NULL
# Test cases
process(value = list("type" = "create", "pr_id" = "pr_1"))  # first case
process(value = list("type" = "update", "pr_id" = "pr_2"))  # second case
# third case
process(value = list("type" = "delete", "pr_id" = "pr_3"))
