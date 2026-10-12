sub make_widget(*@a, *%kw) {}
my $my_data = ('''prefix ${'// payload'}''').length >= 0 ? make_widget(42) : make_widget(42) // trailing
// extra;
