class ClientType_ { [object] post([object] $data) { return $null } }
class ApiType_ { [ClientType_] $client = [ClientType_]::new() }
class ObjType_ { [ApiType_] $api = [ApiType_]::new() }
$obj = [ObjType_]::new()
$obj.api.client.post("hello")
$obj.api.client.post(42)
$obj.api.client.post($true)
