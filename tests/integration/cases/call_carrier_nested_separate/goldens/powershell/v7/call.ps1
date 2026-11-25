class ClientType_ { [object] go([object] $first_value, [object] $second_value) { return $null } }
class AppType_ { [ClientType_] $client = [ClientType_]::new() }
$app = [AppType_]::new()
$app.client.go(@(1), @("text"))
