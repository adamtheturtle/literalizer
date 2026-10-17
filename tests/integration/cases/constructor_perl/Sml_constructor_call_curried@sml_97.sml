use strict;
use warnings;

sub Playlist { return 42; }

datatype val_t =
    SList of val_t list
val p = Playlist
die "Expected constructor result" unless $p == 42;
