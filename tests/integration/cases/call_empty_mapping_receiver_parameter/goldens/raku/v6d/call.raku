class ApiType { method process(*@a, *%kw) {} }
my $api = ApiType.bless;
$api.process({});
