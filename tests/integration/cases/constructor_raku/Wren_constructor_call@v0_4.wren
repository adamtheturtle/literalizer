sub Playlist() { 42 }

var p = Playlist.new()
die "Expected constructor result" unless $p == 42;
