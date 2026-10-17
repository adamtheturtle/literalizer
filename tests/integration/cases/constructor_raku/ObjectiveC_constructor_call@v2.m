sub Playlist() { 42 }

id p = Playlist();
die "Expected constructor result" unless $p == 42;
