sub Playlist() { 42 }

local p = Playlist()
die "Expected constructor result" unless $p == 42;
