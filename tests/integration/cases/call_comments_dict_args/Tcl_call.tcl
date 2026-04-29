proc process {args} {}
# Test cases
process [dict create "type" "create" "pr_id" "pr_1"]  # first case
process [dict create "type" "update" "pr_id" "pr_2"]  # second case
# third case
process [dict create "type" "delete" "pr_id" "pr_3"]
