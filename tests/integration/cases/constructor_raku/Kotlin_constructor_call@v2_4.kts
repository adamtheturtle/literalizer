sub Playlist() { 42 }

val p = Playlist()
die "Expected constructor result" unless $p == 42;
