class OuterType { method inner(*@a, *%kw) {} }
my $outer = OuterType.bless;
$outer.inner(1, 2);
