use strict;
use warnings;

sub Playlist { return 42; }

p := NewPlaylist()
die "Expected constructor result" unless $p == 42;
