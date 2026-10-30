class FooType { method bar(*@a, *%kw) {} }
class FooType { method Foo { FooType.bless } }
my $foo = FooType.bless;
$foo.Foo.bar([1,]);
