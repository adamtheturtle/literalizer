function Playlist { return 42 }

my $p = Playlist();
if ($p -ne 42) { throw "Expected constructor result" }
