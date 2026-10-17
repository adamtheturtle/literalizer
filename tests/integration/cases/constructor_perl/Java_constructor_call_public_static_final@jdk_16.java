use strict;
use warnings;

sub Playlist { return 42; }

public static final Object p = new Playlist();
die "Expected constructor result" unless $p == 42;
