use strict;
use warnings;

sub Playlist { return 42; }

static _VVal p = Playlist();
die "Expected constructor result" unless $p == 42;
