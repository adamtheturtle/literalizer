class ClientType_ { [object] fetch([object] $value) { return $null } }
class AppType_ { [ClientType_] $client = [ClientType_]::new() }
$app = [AppType_]::new()
$app.client.fetch("hello")
$app.client.fetch("world")
