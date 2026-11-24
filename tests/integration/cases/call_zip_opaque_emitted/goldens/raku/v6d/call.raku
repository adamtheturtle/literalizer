sub process(*@a, *%kw) {}
sub emit(*@a, *%kw) {}
emit(process(1), DateTime.new(year => 2024, month => 1, day => 15, hour => 12, minute => 0, second => 0, timezone => 0));
