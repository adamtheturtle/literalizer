sub Playlist() { 42 }

public static final Object p = new Playlist();
die "Expected constructor result" unless $p == 42;
