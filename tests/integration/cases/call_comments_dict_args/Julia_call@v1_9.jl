process(args...; kwargs...) = nothing
# Test cases
process(value=Dict("type" => "create", "pr_id" => "pr_1"))  # first case
process(value=Dict("type" => "update", "pr_id" => "pr_2"))  # second case
# third case
process(value=Dict("type" => "delete", "pr_id" => "pr_3"))
