sub Playlist() { 42 }

public static readonly object? p = new Playlist();
die "Expected constructor result" unless $p == 42;
