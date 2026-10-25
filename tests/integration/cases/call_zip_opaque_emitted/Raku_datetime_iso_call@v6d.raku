sub process(*@a, *%kw) {}
sub emit(*@a, *%kw) {}
emit(process(1), "2024-01-15T12:00:00");
