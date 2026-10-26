class WorkerType_ { [object] process([object] $self, [object] $self_) { return $null } }
class ApiType_ { [WorkerType_] $worker = [WorkerType_]::new() }
$api = [ApiType_]::new()
$api.worker.process(@{}, @{})
