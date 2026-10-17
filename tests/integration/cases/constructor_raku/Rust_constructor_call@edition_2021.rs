sub Playlist() { 42 }

let p = Playlist::new();
die "Expected constructor result" unless $p == 42;
