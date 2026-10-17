sub Playlist() { 42 }

let mut p = Playlist::new();
die "Expected constructor result" unless $p == 42;
