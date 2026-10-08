class ClientType { method fetch(*@a, *%kw) {} }
class AppType { method client { ClientType.bless } }
my $app = AppType.bless;
sub emit(*@a, *%kw) {}
emit($app.client.fetch('hello'));
emit($app.client.fetch(42));
emit($app.client.fetch(True));
