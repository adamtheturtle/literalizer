class MType; def Op(*a, **kw); end; end
m = MType.new
m.Op(operation: {"type" => "create", "pr_id" => "pr_1", "draft" => true})
m.Op(operation: {"type" => "create", "pr_id" => "pr_2"})
