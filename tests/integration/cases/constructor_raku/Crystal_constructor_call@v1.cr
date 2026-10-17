sub Playlist() { 42 }

p = Playlist.new()
die "Expected constructor result" unless $p == 42;
