use JSON::PP;
sub obj {}
sub api {}
sub client {}
sub post {}
obj.api.client.post("hello");
obj.api.client.post(42);
obj.api.client.post(JSON::PP::true);
