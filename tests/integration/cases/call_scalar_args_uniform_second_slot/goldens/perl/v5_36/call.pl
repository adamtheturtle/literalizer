use JSON::PP;
sub process {}
process("hello", "a");
process(42, "b");
process(JSON::PP::true, "c");
