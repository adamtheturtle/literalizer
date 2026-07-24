sub process(*@a, *%kw) {}
sub emit(*@a, *%kw) {}
emit(process(42), 'one');
