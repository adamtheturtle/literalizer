sub process {}
sub emit {}
emit(process("hello"), {"a" => 1, "b" => 2});
emit(process(42), {"c" => 3, "d" => 4});
