class WorkerType { method process(*@a, *%kw) {} }
class ApiType { method worker { WorkerType.bless } }
my $api = ApiType.bless;
$api.worker.process([1, {}], 42);
$api.worker.process([2, {'x' => 's'}], 43);
