class ClientType { method fetch(*@a, *%kw) {} }
class AppType { method client { ClientType.new } }
my $app = AppType.new;
$app.client.fetch('hello');
$app.client.fetch(42);
$app.client.fetch(True);
