class ThingType_ { [object] Before([object] $value) { return $null } }
$thing = [ThingType_]::new()
$thing.Before(1)
