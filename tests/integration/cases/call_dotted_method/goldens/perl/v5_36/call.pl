use JSON::PP;
sub app {}
sub client {}
sub fetch {}
app.client.fetch("hello");
app.client.fetch(42);
app.client.fetch(JSON::PP::true);
