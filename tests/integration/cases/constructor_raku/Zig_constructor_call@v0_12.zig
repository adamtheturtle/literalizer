sub Playlist() { 42 }

const p = Playlist();
die "Expected constructor result" unless $p == 42;
