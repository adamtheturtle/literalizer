sub make_widget(*@a, *%kw) {}
my $my_data = (~/\//).match("/") ? make_widget(42) : null;
