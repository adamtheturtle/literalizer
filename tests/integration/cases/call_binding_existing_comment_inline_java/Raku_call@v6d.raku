sub make_widget(*@a, *%kw) {}
my $my_data = Nil;
$my_data = make_widget(42) // note;
