sub Playlist() { 42 }

public object? p = new Playlist();
die "Expected constructor result" unless $p == 42;
