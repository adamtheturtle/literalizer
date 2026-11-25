class WorkerType { method process(*@a, *%kw) {} }
class ApiType { method worker { WorkerType.bless } }
my $api = ApiType.bless;
$api.worker.process({}, {});
