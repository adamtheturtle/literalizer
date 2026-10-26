sub make_widget(*@a, *%kw) {}
sub consume(*@a, *%kw) {}
my $my_data = make_widget(42, 3);
consume($my_data, 3);
