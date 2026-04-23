sub app {}
sub mgr {}
sub op {}
app.mgr.op({"type" => "create", "pr_id" => "pr_1", "draft" => 1});
app.mgr.op({"type" => "create", "pr_id" => "pr_2"});
