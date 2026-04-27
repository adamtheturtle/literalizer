class MgrType { method op(*@a, *%kw) {} }
class AppType { method mgr { MgrType.new } }
my $app = AppType.new;
$app.mgr.op({'type' => 'create', 'pr_id' => 'pr_1', 'draft' => True});
$app.mgr.op({'type' => 'create', 'pr_id' => 'pr_2'});
