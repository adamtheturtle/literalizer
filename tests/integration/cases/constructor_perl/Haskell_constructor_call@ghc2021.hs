use strict;
use warnings;

sub Playlist { return 42; }

data Val = HList [Val]
p = Playlist
die "Expected constructor result" unless $p == 42;
