use JSON::PP;
sub process {}
sub emit {}
emit(process("hello"), JSON::PP::true);
emit(process(42), JSON::PP::false);
