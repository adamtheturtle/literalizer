proc Playlist {} { return 42 }

protected object? p = new Playlist();
if {$p != 42} { error "Expected constructor result" }
