class ClientType { method post(*@a, *%kw) {} }
class ApiType { method client { ClientType.new } }
class ObjType { method api { ApiType.new } }
my $obj = ObjType.new;
$obj.api.client.post('hello');
$obj.api.client.post(42);
$obj.api.client.post(True);
