class ApiType { method fetch(*@a, *%kw) {} }
class ProcessType { method api { ApiType.bless } }
my $process = ProcessType.bless;
$process.api.fetch({'data' => 'hello'});
$process.api.fetch({'data' => 42});
$process.api.fetch({'data' => True});
