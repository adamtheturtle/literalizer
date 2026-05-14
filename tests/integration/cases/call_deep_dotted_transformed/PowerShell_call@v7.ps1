class ClientType_ { [object] fetch([object] $payload) { return $null } }
class AppType_ { [ClientType_] $client = [ClientType_]::new() }
$app = [AppType_]::new()
function emit {}
emit($app.client.fetch("hello"))
emit($app.client.fetch(42))
emit($app.client.fetch($true))
