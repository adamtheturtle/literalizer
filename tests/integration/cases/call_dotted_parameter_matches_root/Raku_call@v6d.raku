class OuterType { method inner(*@a, *%kw) {} }
my $outer = OuterType.new;
$outer.inner(1, 2);
