sub Playlist() { 42 }

static Object p = new Playlist();
die "Expected constructor result" unless $p == 42;
