class ClientType { method post(*@a, *%kw) {} }
class ApiType { method client { ClientType.bless } }
class ObjType { method api { ApiType.bless } }
my $obj = ObjType.bless;
$obj.api.client.post('hello');
$obj.api.client.post(42);
$obj.api.client.post(True);
