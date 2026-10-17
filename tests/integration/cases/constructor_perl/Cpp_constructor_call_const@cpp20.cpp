use strict;
use warnings;

sub Playlist { return 42; }

const auto p = Playlist();
die "Expected constructor result" unless $p == 42;
