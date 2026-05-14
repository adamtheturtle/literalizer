class Http_clientType { method fetch(*@a, *%kw) {} }
class My_appType { method http_client { Http_clientType.new } }
my $my_app = My_appType.new;
$my_app.http_client.fetch('hello');
$my_app.http_client.fetch(42);
$my_app.http_client.fetch(True);
