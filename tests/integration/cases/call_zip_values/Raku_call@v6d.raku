sub process(*@a, *%kw) {}
sub emit(*@a, *%kw) {}
emit(process('hello'), True);
emit(process(42), False);
