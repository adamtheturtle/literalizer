sub process(*@a, *%kw) {}
sub emit(*@a, *%kw) {}
emit(process('hello'), {'a' => 1, 'b' => 2});
emit(process(42), {'c' => 3, 'd' => 4});
