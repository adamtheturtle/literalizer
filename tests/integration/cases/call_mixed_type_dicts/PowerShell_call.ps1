class MgrType_ { [object] op([object] $operation) { return $null } }
class AppType_ { [MgrType_] $mgr = [MgrType_]::new() }
$app = [AppType_]::new()
$app.mgr.op(@{"type" = "create"; "pr_id" = "pr_1"; "draft" = $true})
$app.mgr.op(@{"type" = "create"; "pr_id" = "pr_2"})
