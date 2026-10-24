class ObjType_ { [object] class([object] $a) { return $null } }
$obj = [ObjType_]::new()
$obj.class(42)
