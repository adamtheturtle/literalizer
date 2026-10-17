sub Playlist() { 42 }

data Val
    = PList (Array Val)
p = Playlist
die "Expected constructor result" unless $p == 42;
