class FooType { method bar(*@a, *%kw) {} }
class FooType { method Foo { FooType.bless } }
class AType { method foo { FooType.bless } }
my $a = AType.bless;
my $my_data = $a.foo.Foo.bar([1,]);
