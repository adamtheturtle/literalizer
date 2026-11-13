class FoobarType { method bar(*@a, *%kw) {} }
class Foo_barType { method fooBar { FoobarType.bless } }
class AType { method foo_bar { Foo_barType.bless } }
my $a = AType.bless;
$a.foo_bar.fooBar.bar([1,]);
