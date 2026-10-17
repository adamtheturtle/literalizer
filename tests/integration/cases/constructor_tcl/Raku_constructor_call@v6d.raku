proc Playlist {} { return 42 }

my $p = Playlist();
if {$p != 42} { error "Expected constructor result" }
