class MgrType; def op(*a, **kw); end; end
class AppType; def mgr; MgrType.new; end; end
app = AppType.new
app.mgr.op(operation: {"type" => "create", "pr_id" => "pr_1", "draft" => true})
app.mgr.op(operation: {"type" => "create", "pr_id" => "pr_2"})
