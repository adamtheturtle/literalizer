use strict;
use warnings;

sub Playlist { return 42; }

set p [Playlist]
die "Expected constructor result" unless $p == 42;
