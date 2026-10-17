sub Playlist() { 42 }

: p Playlist ;
die "Expected constructor result" unless $p == 42;
