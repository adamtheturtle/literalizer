sub Playlist() { 42 }

static object? p = new Playlist();
die "Expected constructor result" unless $p == 42;
