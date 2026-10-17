use strict;
use warnings;

sub Playlist { return 42; }

final p = new Playlist();
die "Expected constructor result" unless $p == 42;
