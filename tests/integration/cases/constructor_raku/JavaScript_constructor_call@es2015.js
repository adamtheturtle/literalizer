sub Playlist() { 42 }

const p = new Playlist({  });
die "Expected constructor result" unless $p == 42;
