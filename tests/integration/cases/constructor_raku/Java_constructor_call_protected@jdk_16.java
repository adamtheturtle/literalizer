sub Playlist() { 42 }

protected Object p = new Playlist();
die "Expected constructor result" unless $p == 42;
