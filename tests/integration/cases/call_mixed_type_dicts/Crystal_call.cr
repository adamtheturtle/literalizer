class MgrType_; def Op(*a, **kw); 0; end; end
mgr = MgrType_.new
mgr.Op(operation: {"type" => "create", "pr_id" => "pr_1", "draft" => true});
mgr.Op(operation: {"type" => "create", "pr_id" => "pr_2"});
