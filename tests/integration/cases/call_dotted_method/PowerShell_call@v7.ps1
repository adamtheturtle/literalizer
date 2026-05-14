class ClientType_ { [object] fetch([object] $payload) { return $null } }
class AppType_ { [ClientType_] $client = [ClientType_]::new() }
$app = [AppType_]::new()
$app.client.fetch("hello")
$app.client.fetch(42)
$app.client.fetch($true)
