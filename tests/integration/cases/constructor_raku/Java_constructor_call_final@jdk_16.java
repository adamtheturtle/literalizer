sub Playlist() { 42 }

final Object p = new Playlist();
die "Expected constructor result" unless $p == 42;
