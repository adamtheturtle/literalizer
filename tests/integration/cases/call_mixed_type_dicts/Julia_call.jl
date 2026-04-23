struct MType; Op; end
m = MType((args...; kwargs...) -> nothing)
m.Op(operation=Dict("type" => "create", "pr_id" => "pr_1", "draft" => true))
m.Op(operation=Dict("type" => "create", "pr_id" => "pr_2"))
