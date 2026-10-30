class FooType_ { [object] bar([object] $x) { return $null } }
class FooType_ { [FooType_] $Foo = [FooType_]::new() }
$foo = [FooType_]::new()
$foo.Foo.bar(@(1))
