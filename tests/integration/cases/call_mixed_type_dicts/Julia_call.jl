struct MgrType; op; end
struct AppType; mgr; end
app = AppType(MgrType((args...; kwargs...) -> nothing))
app.mgr.op(operation=Dict("type" => "create", "pr_id" => "pr_1", "draft" => true))
app.mgr.op(operation=Dict("type" => "create", "pr_id" => "pr_2"))
