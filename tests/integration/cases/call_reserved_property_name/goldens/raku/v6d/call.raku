class FooType { method class(*@a, *%kw) {} }
my $foo = FooType.bless;
$foo.class(1);
