sub process(*@a, *%kw) {}
sub emit(*@a, *%kw) {}
emit(process('hello'), 1);
emit(process(42), 0);
