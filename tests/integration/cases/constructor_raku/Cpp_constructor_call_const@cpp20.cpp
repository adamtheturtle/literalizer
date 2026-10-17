sub Playlist() { 42 }

const auto p = Playlist();
die "Expected constructor result" unless $p == 42;
