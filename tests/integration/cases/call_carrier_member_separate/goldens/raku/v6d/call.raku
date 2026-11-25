class AppType { method go(*@a, *%kw) {} }
my $app = AppType.bless;
$app.go([1,], ['text',]);
