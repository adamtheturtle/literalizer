proc Playlist {} { return 42 }

protected Object p = new Playlist();
if {$p != 42} { error "Expected constructor result" }
