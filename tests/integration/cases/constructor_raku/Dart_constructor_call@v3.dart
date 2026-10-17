sub Playlist() { 42 }

final p = Playlist();
die "Expected constructor result" unless $p == 42;
