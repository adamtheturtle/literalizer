class FooType_ { [object] class([object] $value) { return $null } }
$foo = [FooType_]::new()
$foo.class(1)
