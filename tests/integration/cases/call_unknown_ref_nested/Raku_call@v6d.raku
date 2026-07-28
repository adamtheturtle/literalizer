sub process(*@a, *%kw) {}
my $known_value = True;
my $unknown_value = True;
process($known_value, [$unknown_value]);
