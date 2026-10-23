use JSON::PP;
sub process {}
sub api {}
sub fetch {}
process.api.fetch({"data" => "hello"});
process.api.fetch({"data" => 42});
process.api.fetch({"data" => JSON::PP::true});
