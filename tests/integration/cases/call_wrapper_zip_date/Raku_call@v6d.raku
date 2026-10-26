sub process(*@a, *%kw) {}
sub emit(*@a, *%kw) {}
emit(process(1), Date.new(year => 2024, month => 1, day => 15));
