sub Playlist() { 42 }

static const auto p = Playlist();
die "Expected constructor result" unless $p == 42;
