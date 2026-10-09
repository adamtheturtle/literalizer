class MgrType { method run(*@a, *%kw) {} }
class AppType { method mgr { MgrType.bless } }
my $app = AppType.bless;
$app.mgr.run({'type' => 'create', 'pr_id' => 'pr_1', 'draft' => True});
$app.mgr.run({'type' => 'create', 'pr_id' => 'pr_2'});
