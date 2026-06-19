sub record_value(*@a, *%kw) {}
sub flush_buffer(*@a, *%kw) {}
sub emit(*@a, *%kw) {}
emit(record_value(42));
flush_buffer(3);
