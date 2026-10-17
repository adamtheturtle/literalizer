use strict;
use warnings;

sub Playlist { return 42; }

(def p (Playlist))
die "Expected constructor result" unless $p == 42;
