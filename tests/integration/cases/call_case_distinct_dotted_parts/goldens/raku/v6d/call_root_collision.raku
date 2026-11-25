class FooType1 { method bar(*@a, *%kw) {} }
class FooType0 { method Foo { FooType1.bless } }
my $foo = FooType0.bless;
$foo.Foo.bar([1,]);
