sub Playlist() { 42 }

auto p = Playlist();
die "Expected constructor result" unless $p == 42;
