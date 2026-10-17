use strict;
use warnings;

sub Playlist { return 42; }

type Val =
    | FList of Val list
let p = Playlist()
die "Expected constructor result" unless $p == 42;
