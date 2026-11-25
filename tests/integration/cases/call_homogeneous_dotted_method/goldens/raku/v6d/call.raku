class ClientType { method fetch(*@a, *%kw) {} }
class AppType { method client { ClientType.bless } }
my $app = AppType.bless;
$app.client.fetch('hello');
$app.client.fetch('world');
