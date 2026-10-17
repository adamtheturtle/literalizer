sub Playlist() { 42 }

public Object p = new Playlist();
die "Expected constructor result" unless $p == 42;
