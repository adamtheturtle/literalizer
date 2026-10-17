sub Playlist() { 42 }

p := NewPlaylist()
die "Expected constructor result" unless $p == 42;
