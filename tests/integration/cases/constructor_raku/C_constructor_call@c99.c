sub Playlist() { 42 }

CVal p = Playlist();
die "Expected constructor result" unless $p == 42;
