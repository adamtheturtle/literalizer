class MgrType; def Op(*a, **kw); end; end
mgr = MgrType.new
mgr.Op(operation: {"type" => "create", "pr_id" => "pr_1", "draft" => true})
mgr.Op(operation: {"type" => "create", "pr_id" => "pr_2"})
