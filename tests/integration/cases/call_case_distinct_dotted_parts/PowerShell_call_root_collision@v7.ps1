class FooType_1 { [object] bar([object] $x) { return $null } }
class FooType_0 { [FooType_1] $Foo = [FooType_1]::new() }
$foo = [FooType_0]::new()
$foo.Foo.bar(@(1))
