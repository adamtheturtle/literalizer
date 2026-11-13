class FoobarType_ { [object] bar([object] $x) { return $null } }
class Foo_BarType_ { [FoobarType_] $fooBar = [FoobarType_]::new() }
class AType_ { [Foo_BarType_] $foo_bar = [Foo_BarType_]::new() }
$a = [AType_]::new()
$a.foo_bar.fooBar.bar(@(1))
