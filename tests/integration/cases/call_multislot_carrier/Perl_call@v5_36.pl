use JSON::PP;
sub process {}
process(1, "hello");
process("two", JSON::PP::false);
process((0.0 + 3.5), undef);
