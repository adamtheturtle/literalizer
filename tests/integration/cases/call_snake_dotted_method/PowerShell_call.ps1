class Http_ClientType_ { [object] fetch([object] $payload) { return $null } }
class My_AppType_ { [Http_ClientType_] $http_client = [Http_ClientType_]::new() }
$my_app = [My_AppType_]::new()
$my_app.http_client.fetch("hello")
$my_app.http_client.fetch(42)
$my_app.http_client.fetch($true)
