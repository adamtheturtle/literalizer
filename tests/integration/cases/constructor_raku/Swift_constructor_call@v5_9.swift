sub Playlist() { 42 }

let p = Playlist()
die "Expected constructor result" unless $p == 42;
