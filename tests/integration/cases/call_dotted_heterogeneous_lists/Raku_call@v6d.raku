class ClientType { method go(*@a, *%kw) {} }
class AppType { method client { ClientType.bless } }
my $app = AppType.bless;
$app.client.go([1,], ['text',]);
