class MgrType; def run(*a, **kw); end; end
class AppType; def mgr; MgrType.new; end; end
app = AppType.new
app.mgr.run(operation: {"type" => "create", "pr_id" => "pr_1", "draft" => true})
app.mgr.run(operation: {"type" => "create", "pr_id" => "pr_2"})
