struct MgrType; Op; end
mgr = MgrType((args...; kwargs...) -> nothing)
mgr.Op(operation=Dict("type" => "create", "pr_id" => "pr_1", "draft" => true))
mgr.Op(operation=Dict("type" => "create", "pr_id" => "pr_2"))
