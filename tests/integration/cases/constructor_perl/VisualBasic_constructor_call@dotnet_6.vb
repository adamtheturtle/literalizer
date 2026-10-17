use strict;
use warnings;

sub Playlist { return 42; }

Dim p = New Playlist()
die "Expected constructor result" unless $p == 42;
