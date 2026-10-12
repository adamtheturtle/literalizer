sub make_widget(*@a, *%kw) {}
my $my_data = make_widget(42) // inner
 + 1;
