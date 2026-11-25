use JSON::PP;
sub app {}
sub process {}
sub fetch {}
app.process.fetch({"data" => "hello"});
app.process.fetch({"data" => 42});
app.process.fetch({"data" => JSON::PP::true});
