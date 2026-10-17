sub Playlist() { 42 }

p : A_Val := Playlist;
die "Expected constructor result" unless $p == 42;
