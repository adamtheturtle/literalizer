sub process(*@a, *%kw) {}
my $untyped_value = [];
process([$untyped_value, $untyped_value]);
