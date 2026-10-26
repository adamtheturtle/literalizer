sub f(*@a, *%kw) {}
sub repr(*@a, *%kw) {}
my $ref_data = 1;
repr(f($ref_data));
