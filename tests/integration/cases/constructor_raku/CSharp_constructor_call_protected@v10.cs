sub Playlist() { 42 }

protected object? p = new Playlist();
die "Expected constructor result" unless $p == 42;
