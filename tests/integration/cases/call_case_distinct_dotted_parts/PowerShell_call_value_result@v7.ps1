class FooType_2 { [object] bar([object] $x) { return $null } }
class FooType_1 { [FooType_2] $Foo = [FooType_2]::new() }
class AType_ { [FooType_1] $foo = [FooType_1]::new() }
$a = [AType_]::new()
$my_data = $a.foo.Foo.bar(@(1))
