class FooType2 { method bar(*@a, *%kw) {} }
class FooType1 { method Foo { FooType2.bless } }
class AType { method foo { FooType1.bless } }
my $a = AType.bless;
my $my_data = $a.foo.Foo.bar([1,]);
