class AppType_ { [object] go([object] $first_value, [object] $second_value) { return $null } }
$app = [AppType_]::new()
$app.go(@(1), @("text"))
