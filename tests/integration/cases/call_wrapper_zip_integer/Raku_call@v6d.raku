sub process(*@a, *%kw) {}
sub emit(*@a, *%kw) {}
emit(process(1), 42);
