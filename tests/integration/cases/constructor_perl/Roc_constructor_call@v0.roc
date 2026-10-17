use strict;
use warnings;

sub Playlist { return 42; }

Val : [
    RList (List Val),
]
p = Playlist
die "Expected constructor result" unless $p == 42;
