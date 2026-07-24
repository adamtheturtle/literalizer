sub process(*@a, *%kw) {}
sub emit(*@a, *%kw) {}
emit(process('hello'), 'one');
emit(process(42), 'zero');
