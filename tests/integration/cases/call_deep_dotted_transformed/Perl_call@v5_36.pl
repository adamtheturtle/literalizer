sub app {}
sub client {}
sub fetch {}
sub emit {}
emit(app.client.fetch("hello"));
emit(app.client.fetch(42));
emit(app.client.fetch(1));
