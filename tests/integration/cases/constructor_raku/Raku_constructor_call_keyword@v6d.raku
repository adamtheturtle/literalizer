sub Playlist() { 42 }

my $p = Playlist();
die "Expected constructor result" unless $p == 42;
