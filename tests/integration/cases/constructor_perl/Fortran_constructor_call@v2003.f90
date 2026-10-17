use strict;
use warnings;

sub Playlist { return 42; }

type(fval_t) :: p
p = Playlist()
die "Expected constructor result" unless $p == 42;
