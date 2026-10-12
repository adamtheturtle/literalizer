sub make_widget(*@a, *%kw) {}
my $my_data = ("${{'value': '// payload'}['value']}").length >= 0 ? make_widget(42) : make_widget(42);
