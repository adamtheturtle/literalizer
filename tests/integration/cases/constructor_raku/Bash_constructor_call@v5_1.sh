sub Playlist() { 42 }

declare p="$(Playlist)"
die "Expected constructor result" unless $p == 42;
