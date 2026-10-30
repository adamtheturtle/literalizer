class FooType_ { [object] bar([object] $x) { return $null } }
class FooType_ { [FooType_] $Foo = [FooType_]::new() }
class AType_ { [FooType_] $foo = [FooType_]::new() }
$a = [AType_]::new()
$my_data = $a.foo.Foo.bar(@(1))
