proc Playlist {} { return 42 }

private protected object? p = new Playlist();
if {$p != 42} { error "Expected constructor result" }
