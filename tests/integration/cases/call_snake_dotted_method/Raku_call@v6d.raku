class Http_clientType { method fetch(*@a, *%kw) {} }
class My_appType { method http_client { Http_clientType.bless } }
my $my_app = My_appType.bless;
$my_app.http_client.fetch('hello');
$my_app.http_client.fetch(42);
$my_app.http_client.fetch(True);
