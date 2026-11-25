class WorkerType_ { [object] process([object] $values, [object] $count) { return $null } }
class ApiType_ { [WorkerType_] $worker = [WorkerType_]::new() }
$api = [ApiType_]::new()
$api.worker.process(@(1; @{}), 42)
$api.worker.process(@(2; @{"x" = "s"}), 43)
