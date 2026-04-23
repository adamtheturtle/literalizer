class MType_; def Op(*a, **kw); 0; end; end
m = MType_.new
m.Op(operation: {"type" => "create", "pr_id" => "pr_1", "draft" => true});
m.Op(operation: {"type" => "create", "pr_id" => "pr_2"});
