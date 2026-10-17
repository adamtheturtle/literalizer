use strict;
use warnings;

sub Playlist { return 42; }

private object? p = new Playlist();
die "Expected constructor result" unless $p == 42;
