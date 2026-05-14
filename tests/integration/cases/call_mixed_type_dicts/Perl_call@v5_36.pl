sub app {}
sub mgr {}
sub run {}
app.mgr.run({"type" => "create", "pr_id" => "pr_1", "draft" => 1});
app.mgr.run({"type" => "create", "pr_id" => "pr_2"});
