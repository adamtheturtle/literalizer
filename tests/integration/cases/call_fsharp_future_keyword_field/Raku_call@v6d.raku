class ProcessType { method fetch(*@a, *%kw) {} }
class AppType { method process { ProcessType.bless } }
my $app = AppType.bless;
$app.process.fetch({'data' => 'hello'});
$app.process.fetch({'data' => 42});
$app.process.fetch({'data' => True});
