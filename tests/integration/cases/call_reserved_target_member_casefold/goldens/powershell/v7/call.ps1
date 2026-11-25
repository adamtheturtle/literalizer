class ObjType_ { [object] BEGIN([object] $a) { return $null } }
$obj = [ObjType_]::new()
$obj.BEGIN(42)
